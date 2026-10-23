"""Investigation flows and the main analysis view."""
import streamlit as st

from case_investigator import investigate_case
from .state import init_state, get_uploaded_events, build_investigation
from .theme import apply_theme
from .results import render_results


def run_uploaded_evidence_investigation(events):
    """Investigate uploaded files on their own (no Splunk alert)."""

    with st.status("🤖 AI Investigation Running...", expanded=True) as status:
        status.write("📂 Loading uploaded evidence...")
        status.write("🧠 Retrieving organizational knowledge...")
        status.write("🤖 Running AI investigation...")

        placeholder = {
            "title": "Uploaded Evidence",
            "ip": "N/A",
            "user": "N/A",
            "raw": {},
        }
        status.write("📊 Analyzing evidence...")

        analysis = investigate_case(placeholder, events)

        st.session_state["current_alert"] = build_investigation(
            title="Uploaded Evidence",
            ip="N/A",
            user="N/A",
            analysis=analysis,
            raw={"uploaded_events": events},
            events=events,
        )
        status.update(label="✅ Investigation Complete", state="complete")

    st.session_state["start_uploaded_investigation"] = False
    st.rerun()


def render_investigation_buttons(selected, events):

    col1, col2 = st.columns(2)

    with col1:
        if selected and st.button("🤖 Investigate Alert", use_container_width=True):
            st.session_state["current_alert"] = build_investigation(
                title=selected["title"],
                ip=selected.get("ip", "N/A"),
                user=selected.get("user", "N/A"),
                analysis=selected["analysis"],
                raw=selected["raw"],
                events=events,
            )
            st.rerun()

    with col2:
        if selected and events and st.button(
            "🕵️ Investigate Complete Case",
            type="primary",
            use_container_width=True
        ):
            with st.status("🕵️ Complete Case Investigation Running...", expanded=True) as status:
                status.write("📂 Processing uploaded evidence...")
                status.write("🧠 Retrieving organizational knowledge...")
                status.write("🔍 Analyzing relationships between events...")
                status.write("🤖 Generating AI investigation...")

                analysis = investigate_case(selected, events)

                st.session_state["current_alert"] = build_investigation(
                    title=selected["title"],
                    ip=selected.get("ip", "N/A"),
                    user=selected.get("user", "N/A"),
                    analysis=analysis,
                    raw={
                        "alert": selected["raw"],
                        "uploaded_events": events,
                    },
                    events=events,
                )
                status.update(label="✅ Complete Case Investigation Finished", state="complete")

            st.rerun()


def render_analysis(selected):

    init_state()
    apply_theme()

    uploaded_events = get_uploaded_events()

    # Investigate uploaded evidence (triggered from sidebar)
    if st.session_state["start_uploaded_investigation"]:
        if uploaded_events:
            run_uploaded_evidence_investigation(uploaded_events)
        else:
            st.session_state["start_uploaded_investigation"] = False
            st.error("No events were loaded from the uploaded files.")

    if not selected and not uploaded_events:
        st.info("Upload evidence files or select a Splunk alert.")
        return

    st.markdown('<div class="section-title">🕵️ Investigation</div>', unsafe_allow_html=True)

    render_investigation_buttons(selected, uploaded_events)

    current = st.session_state["current_alert"]

    if current:
        render_results(current)
