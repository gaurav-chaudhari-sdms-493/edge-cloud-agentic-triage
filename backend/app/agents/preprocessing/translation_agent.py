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
                print("=" * 60)
                print("TRANSLATION DEBUG")
                print(f"TRANSLATING FROM: {state.language}")
                print(f"ORIGINAL CONTENT: {state.original_content}")
                
                translated = GoogleTranslator(source=state.language, target='en').translate(state.original_content)
                state.translated_content = translated
                state.content = state.translated_content  # Replace content with translated text for the pipeline
                
                print(f"TRANSLATED CONTENT: {state.translated_content}")
                print("=" * 60)
            except Exception as e:
                state.validation_errors.append(f"Translation failed: {e}")

        return state