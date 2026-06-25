class RouterAgent:

    def run(
        self,
        state
    ):

        state.current_agent="router"

        if (
            state.contains_sensitive
        ):

            state.route="light"

            return state

        if (
            state.input_type
            ==
            "image"
        ):

            state.route="heavy"

            return state

        if (
            state.complexity
            <0.5
        ):

            state.route="light"

        else:
            state.route="heavy"

        return state