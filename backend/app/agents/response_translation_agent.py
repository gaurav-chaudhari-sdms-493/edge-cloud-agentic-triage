from deep_translator import GoogleTranslator
from app.agents.base import AgentState
import json


class ResponseTranslationAgent:
    """
    Translates the agent's final response back to the user's original language.
    If the response is a JSON object, it translates only the string values,
    preserving the English keys.
    """

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "response_translation"
        state.execution_path.append("response_translation")

        if not state.translation_required or state.language == "en":
            return state

        try:
            translator = GoogleTranslator(source='en', target=state.language)

            if isinstance(state.output, dict):
                # It's a dictionary, translate only string values
                translated_output = {}
                for key, value in state.output.items():
                    if isinstance(value, str):
                        translated_output[key] = translator.translate(value)
                    else:
                        # Keep non-string values (like numbers, booleans) as is
                        translated_output[key] = value
                state.output = translated_output
                state.translated_response = json.dumps(translated_output)

            elif isinstance(state.output, str):
                # It's a simple string, translate it directly
                translated_string = translator.translate(state.output)
                state.output = translated_string
                state.translated_response = translated_string

            else:
                # For other data types, convert to string and translate as a fallback
                response_to_translate = str(state.output)
                translated = translator.translate(response_to_translate)
                state.output = translated
                state.translated_response = translated

        except Exception as e:
            state.validation_errors.append(f"Response translation failed: {e}")
            # Fallback to original output if translation fails
            # The original (English) response is better than an error
            print(f"--- Response Translation Error ---")
            print(f"Error: {e}")
            print(f"Original language: {state.language}")
            print(f"Original output: {state.output}")
            print(f"------------------------------------")

        return state
