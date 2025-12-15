"""
LLM utilities: loading the Hugging Face Inference API client and
running generation with a combined system + user prompt.
"""

import os
from functools import lru_cache

from huggingface_hub import InferenceClient

# Smaller, openly accessible model; swap if you prefer another hosted model.
DEFAULT_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"


@lru_cache(maxsize=1)
def load_client(model_name: str = DEFAULT_MODEL_NAME) -> InferenceClient:
    """
    Load and cache the Hugging Face Inference API client.
    Requires HF_TOKEN or HUGGINGFACEHUB_API_TOKEN in the environment.
    """
    hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACEHUB_API_TOKEN")
    if not hf_token:
        raise ValueError("Missing Hugging Face token. Set HF_TOKEN or HUGGINGFACEHUB_API_TOKEN.")

    return InferenceClient(model=model_name, token=hf_token)


def generate_plan(
    prompt: str,
    *,
    model_name: str = DEFAULT_MODEL_NAME,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_new_tokens: int = 512,
) -> str:
    """
    Run generation via chat.completions to support providers that expose only chat.
    The `prompt` should already include the system behavior text.
    """
    client = load_client(model_name)
    completion = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_new_tokens,
    )
    return completion.choices[0].message.content

