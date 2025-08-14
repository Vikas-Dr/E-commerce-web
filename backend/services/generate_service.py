from typing import Optional
import requests
from backend.config import HF_TOKEN, USE_HF_INFERENCE_API, MODEL_GENERATE, MODEL_CHAT


def _require_api():
    if not USE_HF_INFERENCE_API:
        raise RuntimeError("Set HF_TOKEN to use Hugging Face Inference API in this environment.")


def generate_text(prompt: str, context: Optional[str] = None, max_new_tokens: int = 256, temperature: float = 0.7, top_p: float = 0.95) -> str:
    full_prompt = prompt if not context else f"Context: {context}\n\nQuestion: {prompt}\nAnswer:"
    _require_api()
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": full_prompt,
        "parameters": {"max_new_tokens": max_new_tokens, "temperature": temperature, "top_p": top_p},
    }
    url = f"https://api-inference.huggingface.co/models/{MODEL_GENERATE}"
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
        return data[0]["generated_text"]
    if isinstance(data, dict) and "generated_text" in data:
        return data["generated_text"]
    return str(data)


def chat_response(prompt: str, max_new_tokens: int = 256, temperature: float = 0.7, top_p: float = 0.95) -> str:
    _require_api()
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": max_new_tokens, "temperature": temperature, "top_p": top_p},
    }
    url = f"https://api-inference.huggingface.co/models/{MODEL_CHAT}"
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
        return data[0]["generated_text"]
    return str(data)