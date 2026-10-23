import streamlit as st
from api import load_alerts
from utils import normalize_alerts
from ui import render_sidebar, render_metrics, render_alert_table, render_analysis

st.set_page_config(page_title="AI SOC Investigator", page_icon="", layout="wide")
st.markdown("""
<style>

/* Primary Buttons */
.stButton > button {
    background-color: #2563EB !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

.stButton > button:hover {
    background-color: #1D4ED8 !important;
    color: white !important;
}

/* Download Button */
[data-testid="stDownloadButton"] button {
    background-color: #2563EB !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
}

[data-testid="stDownloadButton"] button:hover {
    background-color: #1D4ED8 !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""<style>.block-container{padding-top:1rem;max-width:95%;}</style>""", unsafe_allow_html=True)

alerts = normalize_alerts(load_alerts())

if 'current_alert' not in st.session_state:
    st.session_state.current_alert=None

render_sidebar(alerts)

st.title('AI SOC Investigator')
st.caption('AI-powered security investigation dashboard')

render_metrics(alerts)
st.divider()
selected=render_alert_table(alerts)
st.divider()
render_analysis(selected)
