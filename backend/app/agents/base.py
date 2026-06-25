from dataclasses import dataclass


@dataclass
class AgentState:

    request_id:int

    content:str

    input_type:str

    route:str=None

    complexity:float=0

    confidence:float=0

    output:str=None

    current_agent:str=None
    
    latency_ms:int=0

    contains_sensitive:bool=False

    estimated_cost:int=0

    escalated:bool=False