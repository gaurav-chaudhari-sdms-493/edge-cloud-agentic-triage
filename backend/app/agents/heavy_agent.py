from app.services.llm_service import (
generate
)


class HeavyAgent:

    def run(
        self,
        state
    ):

        state.current_agent=(
            "heavy"
        )

        prompt=f"""

Analyze.

Input:
{state.content}

Return JSON:

summary:
priority:
actions:

Limit:
150 words

"""

        out=generate(

            "qwen2.5:7b",

            prompt
        )

        state.output=out

        state.confidence=.93

        return state