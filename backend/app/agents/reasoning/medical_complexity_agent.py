from app.agents.base import AgentState

class MedicalComplexityAgent:
    """
    Analyzes the query to determine its complexity based on the pre-classified
    intent and an accumulation of keyword scores.
    """

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "medical_complexity"
        
        content_to_analyze = (state.sanitized_content or state.content).lower()
        total_complexity = 0.0

        if state.intent == "emergency":
            total_complexity = 1.0
        elif state.intent == "medical_symptom":
            symptom_scores = {
                "chest pain": 0.4, "chest discomfort": 0.4,
                "shortness of breath": 0.3, "difficulty breathing": 0.3,
                "swelling": 0.2, "fatigue": 0.1,
                "heart": 0.4, "stroke": 0.4, "bleeding": 0.3,
                "diabetes": 0.2, "fever": 0.1, "pain": 0.1, "vomiting": 0.1,
            }
            for keyword, score in symptom_scores.items():
                if keyword in content_to_analyze:
                    total_complexity += score
        
        state.complexity = min(total_complexity, 1.0)
        return state
