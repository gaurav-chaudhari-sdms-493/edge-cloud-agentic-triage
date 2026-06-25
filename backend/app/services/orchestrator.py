import time
from app.agents.base import *
from app.agents.input_agent import *
from app.agents.complexity_agent import *
from app.agents.router_agent import *
from app.agents.light_agent import *
from app.agents.heavy_agent import *
from app.agents.privacy_agent import *
from app.agents.formatter_agent import *


def run_pipeline(req):

    state=AgentState(
        request_id=req.id,
        content=req.content,
        input_type=req.input_type
    )

    start_time = time.time()

    agents=[
        InputAgent(),
        ComplexityAgent(),
        PrivacyAgent(),
        RouterAgent()
    ]

    for a in agents:
        state=a.run(
            state
        )

    if state.route == "light":
        state=(
            LightAgent()
            .run(state)
        )
        if len(state.output) < 40:
            state.route = "heavy"
            state = HeavyAgent().run(state)

    else:
        state=(
            HeavyAgent()
            .run(state)
        )
    
    state.latency_ms = (time.time() - start_time) * 1000

    return (
        FormatterAgent()
        .run(state)
    )