from deep_translator import GoogleTranslator
from app.agents.base import AgentState


class ResponseTranslationAgent:
    """
    Translates the response back to the original language if required.
    """

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "response_translation"
        state.execution_path.append("response_translation")

        if state.translation_required and state.language != "en":
            try:
                # Assuming state.output is a string or can be converted to a string
                response_to_translate = str(state.output)
                translated = GoogleTranslator(source='en', target=state.language).translate(response_to_translate)
                state.translated_response = translated
                state.output = state.translated_response  # Replace output with translated response
            except Exception as e:
                state.validation_errors.append(f"Response translation failed: {e}")

        return state
