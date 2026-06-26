import time
from app.agents.base import AgentState
from app.agents.validation_agent import ValidationAgent
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

PIPELINE = [
    ValidationAgent, OCRAgent, PIIDetectionAgent, PIISanitizationAgent,
    IntentClassificationAgent, MedicalComplexityAgent, UrgencyAssignmentAgent, RouterAgent,
]
# Add the final routed agent to the pipeline for progress calculation
TOTAL_AGENTS = len(PIPELINE) + 1

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
        for i, agent_cls in enumerate(PIPELINE):
            agent_name = agent_cls.__name__.replace('Agent', '').lower()
            update_progress(agent_name, i)
            state = agent_cls().run(state)
            if state.validation_errors:
                state.route = "validation_failed"
                break

        if state.complexity >= 0.8 or state.intent == "emergency":
            state.requires_human_review = True

        if not state.validation_errors:
            routed_agent_cls = LocalKnowledgeAgent if state.route == "local_knowledge" else MedicalReasoningAgent
            agent_name = routed_agent_cls.__name__.replace('Agent', '').lower()
            update_progress(agent_name, len(PIPELINE))
            state = routed_agent_cls().run(state)

        final_output = FormatterAgent().run(state)
        AuditLoggerAgent().run(state) # AuditLogger doesn't need progress update

        return final_output
    finally:
        db.close()
