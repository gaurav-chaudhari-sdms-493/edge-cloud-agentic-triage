from langdetect import detect, LangDetectException
from app.agents.base import AgentState


class LanguageDetectionAgent:
    """
    Detects the language of the content and updates the agent state.
    """

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "language_detection"
        state.execution_path.append("language_detection")

        try:
            # Detect language
            lang = detect(state.content)
            
            # Check if the detected language is supported
            if lang in ["en", "mr", "hi"]:
                state.language = lang
            else:
                # Default to English if the detected language is not supported
                state.language = "en"
                
        except LangDetectException:
            # Default to English if language detection fails
            state.language = "en"

        # Set translation_required flag
        if state.language != "en":
            state.translation_required = True
            state.original_content = state.content
        else:
            state.translation_required = False

        return state
