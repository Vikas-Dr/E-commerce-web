import streamlit as st
import requests

API_BASE = st.secrets.get("API_BASE", "http://localhost:8000")


def call_api(path: str, payload: dict):
    try:
        res = requests.post(f"{API_BASE}{path}", json=payload, timeout=90)
        res.raise_for_status()
        return res.json()
    except Exception as e:  # noqa: BLE001
        st.error(f"API error: {e}")
        return None