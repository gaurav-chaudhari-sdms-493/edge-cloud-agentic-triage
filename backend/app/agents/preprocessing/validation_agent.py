import os
from app.agents.base import AgentState

class ValidationAgent:
    """
    Validates the incoming request data within the AgentState.
    It checks for content presence, supported input types, and file existence for images.
    Errors are logged in the state without raising exceptions.
    """

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "validation"
        state.execution_path.append("validation")

        # 1. Check for empty content
        if not state.content or not state.content.strip():
            state.validation_errors.append("Content is empty.")

        # 2. Check for supported input_type
        supported_types = ["text", "image"]
        if state.input_type not in supported_types:
            state.validation_errors.append(f"Unsupported input_type: '{state.input_type}'. Must be one of {supported_types}.")

        # 3. Check image path if input_type is 'image'
        if state.input_type == "image":
            if not os.path.exists(state.content):
                state.validation_errors.append(f"Image path does not exist: {state.content}")

        return state
