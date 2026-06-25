class FormatterAgent:

    def run(
        self,
        state
    ):

        state.current_agent=(
            "formatter"
        )

        if (
            state.route
            ==
            "light"
        ):
            estimated_cost=(
                round(
                    state.latency_ms
                    /
                    1000,
                    2
                )
            )
        else:
            estimated_cost=(
                round(
                    (
                        state.latency_ms
                        /
                        1000
                    )
                    *
                    2,
                    2
                )
            )

        return {

            "request_id":
            state.request_id,

            "route":
            state.route,

            "complexity":
            state.complexity,

            "confidence":
            state.confidence,

            "agent":
            state.current_agent,

            "result":
            state.output,

            "latency_ms":
            state.latency_ms,

            "used_model":
            (
                "TinyLlama"
                if state.route == "light"
                else "Qwen"
            ),
            "execution_path":[
                "input",
                "complexity",
                "privacy",
                "router",
                state.route,
                "formatter"
            ],
            "estimated_compute_cost": estimated_cost
        }