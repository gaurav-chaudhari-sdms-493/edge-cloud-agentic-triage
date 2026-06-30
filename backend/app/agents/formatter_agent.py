from app.agents.base import AgentState

class FormatterAgent:
    """
    Formats the final output, creating a rich JSON response that provides
    a full, observable trace of the agent pipeline's execution.
    This agent does NOT append itself to the execution path, as it runs last.
    """

    def run(self, state: AgentState) -> dict:
        state.current_agent = "formatter"
        # This agent is the final step, so it's not added to the path itself.

        # Handle the case where validation failed
        if state.validation_errors:
            return {
                "request_id": state.request_id,
                "status": "failed",
                "errors": state.validation_errors,
                "execution_path": state.execution_path,
                "latency_ms": 0, # Latency is added later
            }

        # Format the successful response
        return {
            "request_id": state.request_id,
            "status": "completed",
            "contains_pii": state.contains_pii,
            "detected_entities": state.detected_entities,
            "intent": state.intent,
            "complexity": round(state.complexity, 2),
            "urgency": state.urgency,
            "route": state.route,
            "model_used": state.model_used,
            "latency_ms": 0, # Latency is added later
            "execution_path": state.execution_path,
            "result": state.output,
        }
