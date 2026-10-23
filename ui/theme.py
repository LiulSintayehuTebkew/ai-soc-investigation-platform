"""Visual theme: CSS lives in styles.css, loaded once and cached."""
from functools import lru_cache
from pathlib import Path

import streamlit as st


@lru_cache(maxsize=1)
def _load_css() -> str:
    css = (Path(__file__).parent / "styles.css").read_text(encoding="utf-8")
    return f"<style>{css}</style>"


def apply_theme():
    st.markdown(_load_css(), unsafe_allow_html=True)


def render_hero():
    st.markdown(
        """
        <div class="hero">
            <h1>🛡️ AI SOC Investigator</h1>
            <p>Triage alerts, correlate evidence and let the AI build the case.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
