from app.agents.base import AgentState

class RouterAgent:
    """
    Routes the request to the appropriate downstream agent based on the domain,
    intent, and complexity scores calculated by upstream agents.
    """

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "router"
        state.execution_path.append("router")

        # 1. High complexity queries are always medical
        if state.complexity > 0.8:
            state.route = "medical_reasoning"

        # 2. Route based on the domain (healthcare vs. other)
        elif state.domain == "healthcare":
            # These are simple, non-medical administrative intents.
            admin_intents = {
                "hospital_faq",
                "appointment",
                "appointment_booking",
                "insurance",
                "billing",
                "visiting_hours",
                "departments"
            }
            
            if state.intent in admin_intents:
                state.route = "local_knowledge"
            else:
                # Default for all other healthcare queries (e.g., "What is diabetes?")
                # is the medical reasoning agent.
                state.route = "medical_reasoning"
        else:
            # 3. If the domain is not healthcare, route to local knowledge
            state.route = "local_knowledge"

        print("=" * 60)
        print("ROUTER DEBUG")
        print(f"DOMAIN: {state.domain}")
        print(f"INTENT: {state.intent}")
        print(f"COMPLEXITY: {state.complexity}")
        print(f"FINAL ROUTE: {state.route}")
        print("=" * 60)

        return state