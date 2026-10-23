"""Sidebar: evidence upload, clear/refresh, component status."""
import streamlit as st

from learning_engine import get_knowledge_stats
from .state import init_state, reset_investigation, file_signature
from .theme import apply_theme


def render_sidebar(alerts):

    init_state()
    apply_theme()

    with st.sidebar:

        st.title("🛡️ AI SOC Investigator")

        m1, m2 = st.columns(2)
        stats = get_knowledge_stats()
        m1.metric("Alerts", len(alerts))
        m2.metric("Learned", stats["cases"])

        st.divider()
        st.subheader("Evidence Sources")

        uploaded_files = st.file_uploader(
            "Upload Investigation Files",
            type=["json", "csv", "txt", "log"],
            accept_multiple_files=True
        )

        # Reset investigation only when the uploaded set really changes
        if file_signature(uploaded_files) != file_signature(
            st.session_state["uploaded_files"]
        ):
            reset_investigation()

        st.session_state["uploaded_files"] = uploaded_files or []

        if uploaded_files:

            st.success(f"{len(uploaded_files)} file(s) uploaded")

            with st.expander("View Uploaded Files"):
                for f in uploaded_files:
                    st.write(f"📄 {f.name}")

            if st.button(
                "📂 Investigate Uploaded Evidence",
                type="primary",
                use_container_width=True
            ):
                st.session_state["start_uploaded_investigation"] = True

        st.divider()

        if st.button("🗑️ Clear Investigation", use_container_width=True):
            reset_investigation()
            st.rerun()

        st.divider()
        st.subheader("Active Components")

        chips = "".join(
            f'<span class="chip"><i></i>{c}</span>'
            for c in (
                "📡 Splunk",
                "🤖 Ollama",
                "🔎 IOC Extraction",
                "🔗 Correlation Engine",
                "📄 Incident Reporting",
                "🎯 MITRE ATT&CK",
            )
        )
        st.markdown(chips, unsafe_allow_html=True)

        st.divider()

        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
