# Finance Assistant (FastAPI + Streamlit)

This project implements the architecture in the diagram: a Streamlit UI that calls a FastAPI backend. The backend uses lightweight Hugging Face models (<3B params) for NLU, Q&A, and Chat, with analytics pages for budget and spending insights.

## Models used
- Zero-shot NLU: `MoritzLaurer/deberta-v3-base-zeroshot-v1`
- Q&A / Summaries: `google/flan-t5-base`
- Chatbot: `TinyLlama/TinyLlama-1.1B-Chat-v1.0`

You can run fully local with Transformers or use the Hugging Face Inference API by setting `HF_TOKEN`.

## Setup

```bash
# 1) Create and activate venv (recommended)
python3 -m venv .venv
source .venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) (Optional) Use Hugging Face Inference API for faster startup
export HF_TOKEN=hf_... # your token
```

## Run

Open two terminals:

```bash
# Terminal A: run backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

```bash
# Terminal B: run frontend
streamlit run frontend/streamlit_app.py --server.port 8501
```

Open `http://localhost:8501`.

## Streamlit Pages
- Chatbot: free-form chat.
- Q&A: ask questions with optional context.
- NLU Analysis: zero-shot classification of text into finance intents.
- Budget Summary: upload CSV of transactions and get aggregates + summary.
- Spending Insights: upload CSV and get anomaly detection + insights.

## CSV Format
Columns: `date, amount, category, description`. Expenses are negative amounts; income positive.

## Configuration
You can override default models by setting env vars: `MODEL_NLU`, `MODEL_GENERATE`, `MODEL_CHAT`, `MODEL_SUMMARY`.

## Notes
- If running locally without `HF_TOKEN`, the first run will download models which may take a few minutes.
- All models are <3B params, suitable for CPU-only environments, but performance will vary.