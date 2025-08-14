from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Any
from backend.models.schemas import Transaction, BudgetSummaryResponse, SpendingInsightsResponse
from backend.services.generate_service import generate_text


CATEGORY_NORMALIZATION = {
    "groceries": "Groceries",
    "grocery": "Groceries",
    "food": "Food & Dining",
    "restaurants": "Food & Dining",
    "rent": "Housing",
    "mortgage": "Housing",
    "salary": "Income",
    "paycheck": "Income",
    "transport": "Transport",
    "gas": "Transport",
    "fuel": "Transport",
    "entertainment": "Entertainment",
}


def _normalize_category(raw: str | None) -> str:
    if not raw:
        return "Other"
    key = raw.strip().lower()
    return CATEGORY_NORMALIZATION.get(key, raw.title())


def _safe_month(date_str: str) -> str:
    try:
        d = datetime.fromisoformat(date_str)
        return f"{d.year:04d}-{d.month:02d}"
    except Exception:
        return "Unknown"


def build_budget_summary(transactions: List[Transaction]) -> BudgetSummaryResponse:
    if not transactions:
        return BudgetSummaryResponse(
            total_income=0.0,
            total_expense=0.0,
            net_savings=0.0,
            by_category={},
            by_month={},
            summary_text="No transactions provided.",
        )

    by_category: Dict[str, float] = defaultdict(float)
    by_month: Dict[str, float] = defaultdict(float)
    income = 0.0
    expense = 0.0

    for t in transactions:
        cat = _normalize_category(t.category)
        month = _safe_month(t.date)
        amount = float(t.amount)
        by_category[cat] += amount
        by_month[month] += amount
        if amount > 0:
            income += amount
        else:
            expense += -amount

    net_savings = income - expense

    context = (
        "You are a helpful finance assistant. Summarize the following budget figures in 3-4 bullet points focused on insights and suggestions.\n\n"
        f"Total income: {income:.2f}\n"
        f"Total expenses: {expense:.2f}\n"
        f"Net savings: {net_savings:.2f}\n"
        f"By category: {dict(by_category)}\n"
        f"By month: {dict(by_month)}\n"
    )
    summary_text = generate_text("Provide a concise budget summary.", context=context, max_new_tokens=140)

    return BudgetSummaryResponse(
        total_income=income,
        total_expense=expense,
        net_savings=net_savings,
        by_category=dict(by_category),
        by_month=dict(by_month),
        summary_text=summary_text.strip(),
    )


def build_spending_insights(transactions: List[Transaction]) -> SpendingInsightsResponse:
    if not transactions:
        return SpendingInsightsResponse(insights=[], anomalies=[], summary_text="No data.")

    # Compute per-category totals and simple anomaly detection
    per_cat_amounts: Dict[str, list] = defaultdict(list)
    anomalies: List[Dict[str, Any]] = []

    for t in transactions:
        cat = _normalize_category(t.category)
        amount = float(t.amount)
        if amount < 0:
            per_cat_amounts[cat].append(abs(amount))

    # mean + 2*std threshold per category
    def mean_std(values: list[float]) -> tuple[float, float]:
        if not values:
            return 0.0, 0.0
        m = sum(values) / len(values)
        var = sum((v - m) ** 2 for v in values) / len(values)
        return m, var ** 0.5

    thresholds = {cat: (lambda ms=mean_std(vals): ms[0] + 2 * ms[1])() for cat, vals in per_cat_amounts.items()}

    for t in transactions:
        cat = _normalize_category(t.category)
        amount = float(t.amount)
        if amount < 0:
            th = thresholds.get(cat, 0.0)
            if abs(amount) > th and th > 0:
                anomalies.append({
                    "date": t.date,
                    "amount": amount,
                    "category": cat,
                    "description": t.description or "",
                    "threshold": th,
                })

    top_categories = sorted(((cat, sum(vals)) for cat, vals in per_cat_amounts.items()), key=lambda x: x[1], reverse=True)[:5]
    insights = [
        "Top spending categories: " + ", ".join([f"{k} ({v:.2f})" for k, v in top_categories])
    ]

    context = (
        "You are a finance analyst. Given the anomalies and category totals, provide 3-5 practical spending insights."
        f"\nAnomalies: {anomalies}\nCategory totals: {dict(top_categories)}\n"
    )
    summary_text = generate_text("Write spending insights.", context=context, max_new_tokens=150)

    return SpendingInsightsResponse(
        insights=insights,
        anomalies=anomalies,
        summary_text=summary_text.strip(),
    )