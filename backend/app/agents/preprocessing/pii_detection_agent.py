import re
from app.agents.base import AgentState

class PIIDetectionAgent:
    """
    Detects various types of Personally Identifiable Information (PII) in the
    input content using regular expressions.

    It updates the AgentState with whether PII was found and a list of the
    types of entities detected, but it does not sanitize the content.
    """

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "pii_detection"
        state.execution_path.append("pii_detection")

        # Corrected regex patterns with single backslashes
        patterns = {
            "PHONE": r"\b\d{10}\b|\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
            "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "DOB": r"\b\d{2}/\d{2}/\d{4}\b|\b\d{4}-\d{2}-\d{2}\b",
            "AADHAAR": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
            "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b"
        }

        found_entities = set()

        for entity_type, pattern in patterns.items():
            if re.search(pattern, state.content):
                found_entities.add(entity_type)

        if found_entities:
            state.contains_pii = True
            state.detected_entities = sorted(list(found_entities))

        return state
