import os

# Prefer hosted Hugging Face Inference API if token is provided
HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
USE_HF_INFERENCE_API = bool(HF_TOKEN)

# Lightweight models (< 3B parameters)
# NLU (Zero-shot intent classification)
MODEL_NLU = os.getenv("MODEL_NLU", "MoritzLaurer/deberta-v3-base-zeroshot-v1")

# General text generation / Q&A (encoder-decoder for low compute)
MODEL_GENERATE = os.getenv("MODEL_GENERATE", "google/flan-t5-base")

# Lightweight chat model for free-form chatbot answers
MODEL_CHAT = os.getenv("MODEL_CHAT", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")

# Summarization (we will also use FLAN-T5 for summarization to simplify)
MODEL_SUMMARY = os.getenv("MODEL_SUMMARY", "google/flan-t5-base")

DEFAULT_NLU_LABELS = [
    "budgeting",
    "expense_question",
    "investment_question",
    "savings",
    "spending_insights",
    "general_finance",
    "greeting",
]