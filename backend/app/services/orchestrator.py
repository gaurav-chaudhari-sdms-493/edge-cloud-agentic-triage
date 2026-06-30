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
    DomainClassificationAgent,  # Correctly placed
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

# +3 for routed agent, response translation, and formatter
TOTAL_AGENTS = len(PIPELINE) + 3


def run_pipeline(req):
    start_time = time.time()  # Start latency timer
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

            # Stop early if validation fails or domain is out of scope
            if state.validation_errors:
                state.route = "validation_failed"
                break
            if state.route == "out_of_domain":
                # Domain agent has set the output, so we can stop.
                break
        
        # If the pipeline completed, run the final routed agent
        if not state.validation_errors and state.route not in ["out_of_domain", "validation_failed"]:
            routed_agent_cls = ROUTED_AGENTS.get(state.route)
            if routed_agent_cls:
                agent_name = routed_agent_cls.__name__.replace('Agent', '').lower()
                update_progress(agent_name, len(PIPELINE))
                state = routed_agent_cls().run(state)
            else:
                state.output = "The system could not determine an appropriate route for your request."

        # Set human review flag
        if state.complexity >= 0.8 or state.intent == "emergency":
            state.requires_human_review = True

        # Translate the response
        update_progress("response_translation", len(PIPELINE) + 1)
        state = ResponseTranslationAgent().run(state)

        # Finalize and audit
        update_progress("formatter", len(PIPELINE) + 2)
        # The FormatterAgent should not add its own name to the path
        final_output = FormatterAgent().run(state)
        
        # Calculate and set latency
        end_time = time.time()
        latency_ms = int((end_time - start_time) * 1000)
        final_output['latency_ms'] = latency_ms
        
        # The AuditLoggerAgent runs last and does not update progress
        AuditLoggerAgent(final_output).run(state)

        return final_output
    finally:
        db.close()
