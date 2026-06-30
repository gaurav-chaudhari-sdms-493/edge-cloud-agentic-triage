from app.services.llm_service import generate
from app.agents.base import AgentState

class SimpleMedicalAgent:
    """
    Uses a lightweight LLM (TinyLlama) to answer simple, general-knowledge
    medical questions that are not complex or high-risk.
    """

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "simple_medical"
        state.execution_path.append("simple_medical")

        prompt = f"""
You are a helpful hospital assistant providing general health information.
The user asked: "{state.sanitized_content or state.content}"

**CRITICAL RULES:**
1.  Provide a brief, general, and informative answer.
2.  **DO NOT** offer diagnoses, medical advice, or treatment plans.
3.  If the question is complex, urgent, or asks for specific advice, respond with exactly this sentence: "This question requires a healthcare professional. Please consult a doctor."
4.  Keep your answer to 2-3 sentences.

**Response:**
"""
        llm_output = generate("tinyllama", prompt)
        state.output = llm_output.strip()
        state.model_used = "TinyLlama"

        return state
