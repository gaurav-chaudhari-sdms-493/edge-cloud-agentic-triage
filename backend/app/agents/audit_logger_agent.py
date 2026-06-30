from app.agents.base import AgentState
from app.db.models import AuditLog
from app.core.database import SessionLocal

class AuditLoggerAgent:
    """
    Logs the final state of a request to the database for audit and traceability.
    This is the final agent in the pipeline and receives the final formatted output.
    """

    def __init__(self, final_output: dict):
        self.final_output = final_output

    def run(self, state: AgentState):
        state.current_agent = "audit_logger"
        
        db = SessionLocal()
        try:
            log_entry = AuditLog(
                request_id=state.request_id,
                contains_pii=state.contains_pii,
                detected_entities=state.detected_entities,
                intent=state.intent,
                complexity=state.complexity,
                urgency=state.urgency,
                route=state.route,
                model_used=state.model_used,
                latency_ms=self.final_output.get("latency_ms", 0),
                status=self.final_output.get("status", "unknown"),
                final_result=self.final_output,
                execution_path=state.execution_path,
            )
            db.add(log_entry)
            db.commit()
        finally:
            db.close()
            
        return state
