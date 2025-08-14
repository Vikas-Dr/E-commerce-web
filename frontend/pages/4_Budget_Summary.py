import streamlit as st
import csv
from io import StringIO
import altair as alt
from frontend.utils import call_api

st.header("Budget Summary")
st.markdown("Upload a CSV with columns: date, amount, category, description. Expenses are negative amounts.")

uploaded = st.file_uploader("Transactions CSV", type=["csv"]) 
if uploaded is not None:
	content = uploaded.read().decode("utf-8")
	rows = list(csv.DictReader(StringIO(content)))
	st.dataframe(rows)
	if st.button("Summarize"):
		payload = {"transactions": rows}
		result = call_api("/budget_summary", payload)
		if result:
			col1, col2, col3 = st.columns(3)
			col1.metric("Income", f"{result['total_income']:.2f}")
			col2.metric("Expenses", f"{result['total_expense']:.2f}")
			col3.metric("Net Savings", f"{result['net_savings']:.2f}")
			st.subheader("By Category")
			data_cat = [{"category": k, "amount": v} for k, v in result["by_category"].items()]
			chart_cat = alt.Chart(alt.Data(values=data_cat)).mark_bar().encode(x="category:N", y="amount:Q").properties(height=300)
			st.altair_chart(chart_cat, use_container_width=True)
			st.subheader("By Month")
			data_month = [{"month": k, "amount": v} for k, v in result["by_month"].items()]
			chart_month = alt.Chart(alt.Data(values=data_month)).mark_line(point=True).encode(x="month:N", y="amount:Q").properties(height=300)
			st.altair_chart(chart_month, use_container_width=True)
			st.subheader("Summary")
			st.write(result["summary_text"]) 