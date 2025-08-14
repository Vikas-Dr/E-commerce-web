import streamlit as st

st.set_page_config(page_title="Finance Assistant", page_icon="💸", layout="wide")

st.title("Finance Assistant")

st.markdown(
    "Choose a page from the sidebar: Chatbot, Q&A, NLU Analysis, Budget Summary, Spending Insights."
)

st.markdown(
    "Configure API base via Streamlit secrets: `API_BASE` (default `http://localhost:8000`)."
) 