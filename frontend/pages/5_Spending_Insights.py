import streamlit as st
import csv
from io import StringIO
import altair as alt
from frontend.utils import call_api

st.header("Spending Insights")
st.markdown("Upload a CSV with columns: date, amount, category, description.")

uploaded = st.file_uploader("Transactions CSV", type=["csv"]) 
if uploaded is not None:
	content = uploaded.read().decode("utf-8")
	rows = list(csv.DictReader(StringIO(content)))
	st.dataframe(rows)
	if st.button("Get Insights"):
		payload = {"transactions": rows}
		result = call_api("/spending_insights", payload)
		if result:
			st.subheader("Insights")
			for it in result["insights"]:
				st.write("- " + it)
			if result["anomalies"]:
				st.subheader("Potential Anomalies")
				st.dataframe(result["anomalies"]) 
			st.subheader("Summary")
			st.write(result["summary_text"])