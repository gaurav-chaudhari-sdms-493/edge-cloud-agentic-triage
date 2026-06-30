from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class AgentState:
    # Existing fields
    request_id: int
    content: str
    input_type: str
    route: str = None
    complexity: float = 0
    confidence: float = 0
    output: Any = None  # Can be string or dict
    current_agent: str = None
    latency_ms: int = 0
    estimated_cost: int = 0
    escalated: bool = False

    # Fields for healthcare privacy workflow
    sanitized_content: str = ""
    contains_pii: bool = False
    detected_entities: List[str] = field(default_factory=list)
    intent: str = "unknown"
    urgency: str = "low"
    validation_errors: List[str] = field(default_factory=list)
    model_used: str = ""
    execution_path: List[Dict[str, Any]] = field(default_factory=list)
    
    # New field for human review flag
    requires_human_review: bool = False

    # Domain classification fields
    domain: str = "unknown"
    supported_domain: bool = False
    domain_confidence: float = 0.0

    # Multilingual support fields
    language: str = "en"
    translation_required: bool = False
    original_content: str = ""
    translated_content: str = ""
    translated_response: str = ""
