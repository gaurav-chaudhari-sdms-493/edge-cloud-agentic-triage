import re


class PrivacyAgent:

    def run(
        self,
        state
    ):

        state.current_agent=(
            "privacy"
        )

        patterns=[

            r"\\d{10}",

            r"\\S+@\\S+"

        ]

        sensitive=False

        for p in patterns:

            if (
                re.search(
                    p,
                    state.content
                )
            ):

                sensitive=True

        state.contains_sensitive=(
            sensitive
        )

        return state