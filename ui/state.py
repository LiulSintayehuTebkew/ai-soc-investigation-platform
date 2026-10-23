"""Session state and investigation record helpers."""
import streamlit as st

from ioc_extractor import extract_iocs
from utils import build_incident_report
from log_loader import load_uploaded_logs


STATE_DEFAULTS = {
    "uploaded_files": [],
    "uploaded_events": [],
    "_events_signature": None,
    "current_alert": None,
    "start_uploaded_investigation": False,
}


def init_state():
    for key, value in STATE_DEFAULTS.items():
        st.session_state.setdefault(key, value)


def reset_investigation():
    st.session_state["current_alert"] = None
    st.session_state["start_uploaded_investigation"] = False


def file_signature(files):
    """Cheap fingerprint of the uploaded files (name + size)."""
    return tuple((f.name, f.size) for f in files) if files else ()


def get_uploaded_events():
    """
    Parse uploaded files only when the set of files changes,
    instead of on every Streamlit rerun.
    """
    files = st.session_state["uploaded_files"]
    signature = file_signature(files)

    if st.session_state["_events_signature"] != signature:
        st.session_state["uploaded_events"] = (
            load_uploaded_logs(files) if files else []
        )
        st.session_state["_events_signature"] = signature

    return st.session_state["uploaded_events"]


def build_investigation(title, ip, user, analysis, raw, events):
    """
    Build the investigation record once and precompute everything the
    tabs need (correlations, IOCs, report), so tab rendering and
    reruns stay cheap.
    """
    current = {
        "title": title,
        "ip": ip,
        "user": user,
        "analysis": analysis,
        "raw": raw,
    }

    current["iocs"] = extract_iocs(raw)
    current["report"] = build_incident_report(current)

    return current
