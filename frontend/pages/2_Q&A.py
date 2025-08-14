import streamlit as st
from frontend.utils import call_api

st.header("Q&A")
question = st.text_area("Ask a finance question", "What is a 50/30/20 budget?", height=120)
context = st.text_area("Optional context", "", height=100)
if st.button("Answer"):
	data = {"prompt": question, "context": context, "max_new_tokens": 200}
	result = call_api("/generate", data)
	if result:
		st.write(result.get("text", ""))