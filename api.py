import requests
import streamlit as st

API_URL = "http://127.0.0.1:5000/alerts"

@st.cache_data(ttl=5)
def load_alerts():

    try:

        response = requests.get(
            API_URL,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        print(e)

        return []