import time
from app.agents.base import AgentState
from app.agents.validation_agent import ValidationAgent
from app.agents.language_detection_agent import LanguageDetectionAgent
from app.agents.translation_agent import TranslationAgent
from app.agents.response_translation_agent import ResponseTranslationAgent
from app.agents.domain_classification_agent import DomainClassificationAgent
from app.agents.ocr_agent import OCRAgent
from app.agents.pii_detection_agent import PIIDetectionAgent
from app.agents.pii_sanitization_agent import PIISanitizationAgent
from app.agents.intent_classification_agent import IntentClassificationAgent
from app.agents.medical_complexity_agent import MedicalComplexityAgent
from app.agents.urgency_assignment_agent import UrgencyAssignmentAgent
from app.agents.router_agent import RouterAgent
from app.agents.local_knowledge_agent import LocalKnowledgeAgent
from app.agents.medical_reasoning_agent import MedicalReasoningAgent
from app.agents.formatter_agent import FormatterAgent
from app.agents.audit_logger_agent import AuditLoggerAgent
from app.core.database import SessionLocal
from app.db.models import Request

# The main pipeline of agents that run in sequence.
PIPELINE = [
    ValidationAgent,
    LanguageDetectionAgent,
    TranslationAgent,
    DomainClassificationAgent,
    OCRAgent,
    PIIDetectionAgent,
    PIISanitizationAgent,
    IntentClassificationAgent,
    MedicalComplexityAgent,
    UrgencyAssignmentAgent,
    RouterAgent,
]

# Map route names to the final agent classes that can be called.
ROUTED_AGENTS = {
    "local_knowledge": LocalKnowledgeAgent,
    "medical_reasoning": MedicalReasoningAgent,
}

TOTAL_AGENTS = len(PIPELINE) + 1  # +1 for the final routed agent


def run_pipeline(req):
    state = AgentState(request_id=req.id, content=req.content, input_type=req.input_type)
    db = SessionLocal()

    def update_progress(agent_name, agent_index):
        progress_percentage = int(((agent_index + 1) / TOTAL_AGENTS) * 100)
        db.query(Request).filter(Request.id == req.id).update({
            "current_agent": agent_name,
            "progress": progress_percentage
        })
        db.commit()

    try:
        # Run the main sequential pipeline
        for i, agent_cls in enumerate(PIPELINE):
            agent_name = agent_cls.__name__.replace('Agent', '').lower()
            update_progress(agent_name, i)
            state = agent_cls().run(state)
            # If validation fails, we stop early.
            if state.validation_errors:
                state.route = "validation_failed"
                break
        
        # If the pipeline completed without validation errors, run the final routed agent
        if not state.validation_errors:
            routed_agent_cls = ROUTED_AGENTS.get(state.route)
            if routed_agent_cls:
                agent_name = routed_agent_cls.__name__.replace('Agent', '').lower()
                update_progress(agent_name, len(PIPELINE))
                state = routed_agent_cls().run(state)
            else:
                # If the router returns an unknown route, handle it gracefully
                state.output = "The system could not determine an appropriate route for your request."

        # Set human review flag for high complexity or emergency cases
        if state.complexity >= 0.8 or state.intent == "emergency":
            state.requires_human_review = True

        # Translate the response if needed
        state = ResponseTranslationAgent().run(state)

        # Finalize and audit the results
        final_output = FormatterAgent().run(state)
        AuditLoggerAgent().run(state)

        return final_output
    finally:
        db.close()
