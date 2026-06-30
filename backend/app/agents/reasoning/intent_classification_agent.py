from app.agents.base import AgentState

class IntentClassificationAgent:
    """
    Classifies the user's intent based on keyword matching.
    This version uses simple substring matching for robustness and includes
    detailed debugging prints.
    """

    def _get_intent(self, content_to_analyze: str) -> str:
        """
        Determines the intent from the content by checking for keywords in a prioritized order.
        """
        # The order of intents matters. More specific and critical intents should come first.
        intent_keywords = {
            "medical_reasoning": [
                "chief complaint", "visit summary", "temperature", "labs", "test result",
                "diagnosis", "vitals", "assessment", "plan", "medication", "positive", 
                "negative", "abnormal", "report", "scan", "x-ray", "mri"
            ],
            "emergency": ["chest pain", "breathing", "severe bleed", "unconscious", "accident"],
            "appointment": ["appointment", "book", "schedule", "meet a doctor"],
            "insurance": ["insurance", "claim", "policy", "coverage", "billing"],
            "medical_symptom": ["fever", "cough", "headache", "pain", "vomit", "dizzy", "nausea", "symptom"],
            "hospital_faq": ["hours", "timing", "address", "contact", "departments", "visiting"],
        }

        print("=" * 60)
        print("INTENT CLASSIFICATION DEBUG")
        print(f"CONTENT: {repr(content_to_analyze)}")

        for intent, keywords in intent_keywords.items():
            print(f"\nChecking intent: {intent}")
            for keyword in keywords:
                match = keyword in content_to_analyze
                print(f"  - '{keyword}': {'MATCH' if match else 'no match'}")
                if match:
                    print(f"\nFINAL DETECTED INTENT: {intent}")
                    print("=" * 60)
                    return intent
        
        print("\nFINAL DETECTED INTENT: other")
        print("=" * 60)
        return "other"

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "intent_classification"
        state.execution_path.append("intent_classification")

        content_to_analyze = (state.sanitized_content or state.content).lower()
        
        detected_intent = self._get_intent(content_to_analyze)

        state.intent = detected_intent
        return state
