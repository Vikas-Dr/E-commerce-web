from typing import List, Optional
from pydantic import BaseModel, Field


class TextPayload(BaseModel):
    text: str
    candidate_labels: Optional[List[str]] = None


class NluResponse(BaseModel):
    labels: List[str]
    scores: List[float]


class GeneratePayload(BaseModel):
    prompt: str
    context: Optional[str] = None
    max_new_tokens: int = 256
    temperature: float = 0.7
    top_p: float = 0.95
    mode: Optional[str] = Field(default=None, description="Use 'chat' to force chat model")


class GenerateResponse(BaseModel):
    text: str


class Transaction(BaseModel):
    date: str
    amount: float
    category: Optional[str] = None
    description: Optional[str] = None


class BudgetSummaryPayload(BaseModel):
    transactions: List[Transaction]


class BudgetSummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    net_savings: float
    by_category: dict
    by_month: dict
    summary_text: str


class SpendingInsightsPayload(BaseModel):
    transactions: List[Transaction]


class SpendingInsightsResponse(BaseModel):
    insights: List[str]
    anomalies: List[dict]
    summary_text: str