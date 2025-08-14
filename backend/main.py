from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from backend.models.schemas import (
    TextPayload,
    NluResponse,
    GeneratePayload,
    GenerateResponse,
    BudgetSummaryPayload,
    BudgetSummaryResponse,
    SpendingInsightsPayload,
    SpendingInsightsResponse,
)
from backend.services.nlu_service import classify_intent
from backend.services.generate_service import generate_text, chat_response
from backend.services.finance_service import build_budget_summary, build_spending_insights

app = FastAPI(title="Finance Assistant API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "Finance Assistant API running"}


@app.post("/nlu", response_model=NluResponse)
def nlu_endpoint(payload: TextPayload):
    try:
        result = classify_intent(payload.text, payload.candidate_labels)
        return NluResponse(labels=result["labels"], scores=result["scores"]) 
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/generate", response_model=GenerateResponse)
def generate_endpoint(payload: GeneratePayload):
    try:
        if payload.mode == "chat":
            text = chat_response(payload.prompt, max_new_tokens=payload.max_new_tokens, temperature=payload.temperature, top_p=payload.top_p)
        else:
            text = generate_text(payload.prompt, context=payload.context, max_new_tokens=payload.max_new_tokens, temperature=payload.temperature, top_p=payload.top_p)
        return GenerateResponse(text=text)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/budget_summary", response_model=BudgetSummaryResponse)
def budget_summary_endpoint(payload: BudgetSummaryPayload):
    try:
        summary = build_budget_summary(payload.transactions)
        return summary
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/spending_insights", response_model=SpendingInsightsResponse)
def spending_insights_endpoint(payload: SpendingInsightsPayload):
    try:
        insights = build_spending_insights(payload.transactions)
        return insights
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc))