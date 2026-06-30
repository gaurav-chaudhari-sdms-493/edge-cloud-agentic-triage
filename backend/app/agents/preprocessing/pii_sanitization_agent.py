import re
from app.agents.base import AgentState

class PIISanitizationAgent:
    """
    Sanitizes the input content by replacing detected PII with placeholders.
    This agent runs unconditionally for defense-in-depth, ensuring that
    even if the detection agent misses something, sanitization is still attempted.
    """

    def run(self, state: AgentState) -> AgentState:
        state.current_agent = "pii_sanitization"
        state.execution_path.append("pii_sanitization")

        # Corrected regex patterns with single backslashes
        patterns = {
            r"\b\d{10}\b|\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}": "[PHONE]",
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b": "[EMAIL]",
            r"\b\d{2}/\d{2}/\d{4}\b|\b\d{4}-\d{2}-\d{2}\b": "[DOB]",
            r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b": "[AADHAAR]",
            r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b": "[PAN]"
        }

        sanitized_version = state.content
        for pattern, placeholder in patterns.items():
            sanitized_version = re.sub(pattern, placeholder, sanitized_version)

        state.sanitized_content = sanitized_version

        return state
