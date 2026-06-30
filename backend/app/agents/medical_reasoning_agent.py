import json
from app.services.llm_service import generate
from app.agents.base import AgentState


class MedicalReasoningAgent:
    """
    Uses a powerful LLM (Qwen) to analyze complex medical queries.
    It attempts to parse the LLM's string output into a JSON object,
    making the final result structured and resilient to malformed output.
    """

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "medical_reasoning"
        state.execution_path.append("medical_reasoning")

        prompt = f"""
You are a hospital triage assistant. Your task is to analyze a user's query and return a single, valid JSON object.

User query: "{state.sanitized_content or state.content}"

**CRITICAL RULES:**
1.  Your response MUST be ONLY the JSON object. Do not include any introductory text, markdown, or any characters outside of the JSON structure.
2.  Never diagnose a medical condition.
3.  Never prescribe or recommend specific medicines.

The JSON object must have these exact keys:
- "summary": A brief, neutral summary of the user's stated symptoms.
- "risk_level": Your assessment of the risk level. Choose one: "Low", "Medium", "High", "Emergency".
- "recommended_next_step": A safe, general next step for the user. Example: "Consult a healthcare professional within 24 hours."

Example of a perfect response:
{{"summary": "User reports a headache and mild fever.", "risk_level": "Low", "recommended_next_step": "Monitor symptoms and rest."}}
"""

        llm_output_str = generate(
            profile_name="medical_reasoning",
            prompt=prompt
        )

        # Attempt to parse the LLM output string into a JSON object
        try:
            # Clean up potential markdown code fences
            cleaned_output = llm_output_str.strip().replace("```json", "").replace("```", "").strip()
            parsed_output = json.loads(cleaned_output)
            state.output = parsed_output
        except json.JSONDecodeError as e:
            print(f"--- JSON PARSE ERROR in MedicalReasoningAgent ---")
            print(f"Error: {e}")
            print(f"Original LLM Output: {repr(llm_output_str)}")
            print(f"-------------------------------------------------")
            # If parsing fails, store the raw string and log the error
            state.output = {"error": "LLM returned malformed JSON.", "raw_output": llm_output_str}

        state.model_used = "Qwen"

        return state