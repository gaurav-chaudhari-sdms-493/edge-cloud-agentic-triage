import json
import os
from app.agents.base import AgentState

class LocalKnowledgeAgent:
    """
    Handles simple, non-medical queries using a deterministic JSON lookup.
    """

    def __init__(self):
        kb_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'hospital_kb.json')
        with open(kb_path, 'r') as f:
            self.knowledge_base = json.load(f)

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "local_knowledge"
        
        # Directly use the classified intent to look up the answer.
        # This agent should only handle known, deterministic queries.
        if state.intent in self.knowledge_base:
            state.output = self.knowledge_base[state.intent]["answer"]
            state.model_used = "KnowledgeBase"
        else:
            # If the intent is not in our KB, we provide a standard fallback.
            # This avoids unpredictable LLM behavior for this route.
            state.output = "Please contact our help desk for assistance with your request."
            state.model_used = "Fallback"

        return state
