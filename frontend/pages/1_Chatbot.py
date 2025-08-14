import streamlit as st
from frontend.utils import call_api

st.header("Chatbot")
with st.form("chat_form"):
	prompt = st.text_area("Your message", "How can I save more each month?", height=120)
	submitted = st.form_submit_button("Send")
if submitted and prompt.strip():
	data = {"prompt": prompt, "mode": "chat", "max_new_tokens": 200}
	result = call_api("/generate", data)
	if result:
		st.write(result.get("text", ""))