import json
import os
import re
from app.services.llm_service import generate
from app.agents.base import AgentState

class LocalKnowledgeAgent:
    """
    Handles simple, non-medical queries using a deterministic JSON lookup.
    If no direct match is found, it falls back to a lightweight LLM (TinyLlama)
    with a robust, structured prompt.
    """

    def __init__(self):
        kb_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'hospital_kb.json')
        with open(kb_path, 'r') as f:
            self.knowledge_base = json.load(f)

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "local_knowledge"
        
        content_to_analyze = (state.sanitized_content or state.content).lower()
        
        found_in_kb = False
        for key, entry in self.knowledge_base.items():
            for keyword in entry["keywords"]:
                if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', content_to_analyze):
                    state.output = entry["answer"]
                    state.model_used = "KnowledgeBase"
                    found_in_kb = True
                    break
            if found_in_kb:
                break

        if not found_in_kb:
            # This new prompt is much more explicit and less likely to be ignored.
            prompt = f"""
You are a hospital administrative assistant AI. Your ONLY function is to answer simple administrative questions.

User query: "{content_to_analyze}"

**CRITICAL RULES:**
1.  Analyze the user's query to determine if it is about one of these topics: hospital timings, appointments, departments, billing, or insurance.
2.  If the query is about one of those topics, provide a brief, helpful answer.
3.  If the query is about ANY other topic (especially medical symptoms, conditions, or advice), you MUST respond with ONLY the following exact sentence: "This request requires medical triage."
4.  Do not apologize or add any extra words.

Your response:
"""
            llm_output = generate(
                "tinyllama",
                prompt
            )
            state.output = llm_output
            state.model_used = "TinyLlama"

        return state
