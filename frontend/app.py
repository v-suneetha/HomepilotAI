import os

import requests
import streamlit as st

if os.getenv("RUNNING_IN_DOCKER") == "true":
    BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
else:
    BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="HomePilot AI", page_icon="🏠")
st.title("HomePilot AI")
st.write("Local AI household operating system")

try:
    response = requests.get(f"{BACKEND_URL}/health", timeout=5)
    if response.ok:
        payload = response.json()
        st.success(f"Backend connected: {payload['service']}")
    else:
        st.warning("Backend responded with an error")
except Exception as exc:
    st.error(f"Unable to reach backend: {exc}")
