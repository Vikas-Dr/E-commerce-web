import streamlit as st
import pandas as pd
from frontend.utils import call_api

st.header("NLU Analysis (Zero-shot)")
text = st.text_area("Text", "Show me my grocery spend this month and suggest a budget.", height=120)
labels = st.text_input("Candidate labels (comma separated)", "budgeting, expense_question, investment_question, savings, spending_insights, general_finance")
if st.button("Classify"):
	candidate_labels = [x.strip() for x in labels.split(",") if x.strip()]
	payload = {"text": text, "candidate_labels": candidate_labels}
	result = call_api("/nlu", payload)
	if result:
		df = pd.DataFrame({"label": result["labels"], "score": result["scores"]})
		st.dataframe(df)