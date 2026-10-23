"""Result tabs: investigation, organizational memory, IOCs, raw data."""
import streamlit as st

from learning_engine import save_case_knowledge
from rag_context import get_rag_context


@st.fragment
def render_download_button(report_data):
    st.download_button(
        "📄 Download Report",
        report_data,
        "incident_report.md",
        use_container_width=True
    )


def render_results(current):

    context = get_rag_context(current)

    st.write("")

    tab_investigation, tab_memory, tab_iocs, tab_raw = st.tabs([
        "🕵️ Investigation",
        "🧠 Organizational Memory",
        "🔎 IOCs",
        "📋 Raw Data"
    ])

    # ==================================================
    # INVESTIGATION TAB
    # ==================================================

    with tab_investigation:

        with st.container(border=True):
            st.markdown(current["analysis"])

        # Render isolated download fragment
        render_download_button(current["report"])

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "✅ Confirmed Attack",
                use_container_width=True,
                key=f"confirm_{current['title']}"
            ):
                save_case_knowledge(
                    current,
                    current["analysis"],
                    "confirmed_attack"
                )
                st.success("Stored in organizational knowledge base.")

        with col2:
            if st.button(
                "❌ False Positive",
                use_container_width=True,
                key=f"fp_{current['title']}"
            ):
                save_case_knowledge(
                    current,
                    current["analysis"],
                    "false_positive"
                )
                st.success("Stored as false positive.")

    # ==================================================
    # ORGANIZATIONAL MEMORY TAB
    # ==================================================

    with tab_memory:

        st.subheader("✅ Similar Confirmed Attacks")

        confirmed_cases = context.get("confirmed", [])

        if confirmed_cases:
            for i, case in enumerate(confirmed_cases, start=1):
                with st.expander(f"Confirmed Case #{i}"):
                    st.markdown(case)
        else:
            st.info("No similar confirmed attacks found.")

        st.divider()

        st.subheader("❌ Similar False Positives")

        false_positive_cases = context.get("false_positive", [])

        if false_positive_cases:
            for i, case in enumerate(false_positive_cases, start=1):
                with st.expander(f"False Positive #{i}"):
                    st.markdown(case)
        else:
            st.info("No similar false positives found.")

    # ==================================================
    # IOC TAB
    # ==================================================

    with tab_iocs:
        with st.container(border=True):
            st.json(current["iocs"])

    # ==================================================
    # RAW TAB
    # ==================================================

    with tab_raw:
        with st.container(border=True):
            st.json(current["raw"])
