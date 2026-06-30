import ollama
from app.core.llm_config import LLM_PROFILES


def generate(profile_name, prompt, model=None):
    """
    Generates a response from an LLM using predefined profiles or backward-compatible parameters.

    Args:
        profile_name (str): The name of the LLM profile to use (e.g., "medical_reasoning").
                            For backward compatibility, this can also be a model name.
        prompt (str): The input prompt for the LLM.
        model (str, optional): If provided, this overrides the profile and uses a default
                               configuration for the specified model. Defaults to None.

    Returns:
        str: The content of the LLM's response, or a timeout message on error.
    """
    # Prioritize the explicit 'model' parameter for backward compatibility
    if model:
        config = {
            "model": model,
            "temperature": 0.2,
            "num_predict": 180,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1
        }
    # Use the profile if it exists
    elif profile_name in LLM_PROFILES:
        config = LLM_PROFILES[profile_name]
    # Fallback for legacy calls where profile_name was the model name
    else:
        config = {
            "model": profile_name,
            "temperature": 0.2,
            "num_predict": 180,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1
        }

    try:
        res = ollama.chat(
            model=config["model"],
            options={
                "temperature": config.get("temperature", 0.2),
                "top_p": config.get("top_p", 0.9),
                "top_k": config.get("top_k", 40),
                "repeat_penalty": config.get("repeat_penalty", 1.1),
                "num_predict": config.get("num_predict", 180)
            },
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return res["message"]["content"]
    except Exception as e:
        print(f"Error during model generation: {e}")
        return "model timeout"
