"""
Centralized configuration for Large Language Model (LLM) parameters.

This module defines profiles for different LLM use cases, allowing for easy
management and extension of model configurations without changing the service code.
"""

LLM_PROFILES = {
    "medical_reasoning": {
        "model": "qwen2.5:7b",
        "temperature": 0.1,  # Low temperature for more deterministic and fact-based responses
        "top_p": 0.9,
        "top_k": 40,
        "repeat_penalty": 1.1,
        "num_predict": 300,  # Higher token limit for detailed medical reasoning
    },
    "knowledge_base": {
        "model": "tinyllama",
        "temperature": 0.0,  # Zero temperature for precise, factual answers from the knowledge base
        "top_p": 1.0,
        "top_k": 20,
        "repeat_penalty": 1.0,
        "num_predict": 120,  # Shorter responses for concise information retrieval
    },
    # Future profiles can be added here without changing the service code.
    # "translation": { ... },
    # "ocr_correction": { ... },
    # "summarization": { ... },
}
