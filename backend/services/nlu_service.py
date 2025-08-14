from typing import List, Dict
import requests
from backend.config import HF_TOKEN, USE_HF_INFERENCE_API, MODEL_NLU, DEFAULT_NLU_LABELS


def classify_intent(text: str, candidate_labels: List[str] | None) -> Dict[str, List]:
    labels = candidate_labels or DEFAULT_NLU_LABELS
    if not USE_HF_INFERENCE_API:
        raise RuntimeError("Set HF_TOKEN to use Hugging Face Inference API in this environment.")

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    data = {
        "inputs": text,
        "parameters": {"candidate_labels": labels},
    }
    url = f"https://api-inference.huggingface.co/models/{MODEL_NLU}"
    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()
    payload = response.json()
    return {"labels": payload["labels"], "scores": payload["scores"]}