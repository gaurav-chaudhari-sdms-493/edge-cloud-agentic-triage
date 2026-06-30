from deep_translator import GoogleTranslator
from app.agents.base import AgentState


class TranslationAgent:
    """
    Translates content to English if required.
    """

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "translation"
        state.execution_path.append("translation")

        if state.translation_required and state.language != "en":
            try:
                translated = GoogleTranslator(source=state.language, target='en').translate(state.original_content)
                state.translated_content = translated
                state.content = state.translated_content  # Replace content with translated text for the pipeline
            except Exception as e:
                state.validation_errors.append(f"Translation failed: {e}")

        return state
