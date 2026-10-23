"""KPI cards and the searchable alert table."""
import pandas as pd
import streamlit as st

from .theme import apply_theme, render_hero


def render_metrics(alerts):

    apply_theme()
    render_hero()

    ips = {a.get("ip") for a in alerts} - {None, "N/A"}
    users = {a.get("user") for a in alerts} - {None, "N/A"}

    c1, c2, c3 = st.columns(3)

    c1.metric("🚨 Alerts", len(alerts))
    c2.metric("🌐 Source IPs", len(ips))
    c3.metric("👤 Users", len(users))

    st.write("")


TABLE_COLUMNS = ["Alert", "Source IP", "User", "Severity"]


def render_alert_table(alerts):

    if not alerts:
        st.info("No alerts currently available.")
        return None

    st.markdown('<div class="section-title">🚨 Alert Queue</div>', unsafe_allow_html=True)

    df = pd.DataFrame(
        {
            "Alert": [a.get("title", "N/A") for a in alerts],
            "Source IP": [a.get("ip", "N/A") for a in alerts],
            "User": [a.get("user", "N/A") for a in alerts],
            "Severity": [a.get("severity", "N/A") for a in alerts],
            "_idx": range(len(alerts)),
        }
    )

    search = st.text_input(
        "Search Alerts",
        placeholder="🔍  Filter by alert, IP, user or severity..."
    )

    if search:
        # Vectorised search across the visible columns
        blob = df[TABLE_COLUMNS[0]].astype(str)
        for col in TABLE_COLUMNS[1:]:
            blob = blob + " " + df[col].astype(str)

        df = df[blob.str.contains(search, case=False, regex=False)]

    event = st.dataframe(
        df[TABLE_COLUMNS],
        use_container_width=True,
        height=350,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            "Alert": st.column_config.TextColumn("Alert", width="large"),
            "Source IP": st.column_config.TextColumn("🌐 Source IP"),
            "User": st.column_config.TextColumn("👤 User"),
            "Severity": st.column_config.TextColumn("⚠️ Severity"),
        },
    )

    selected_rows = event.selection.rows

    if selected_rows:
        return alerts[int(df.iloc[selected_rows[0]]["_idx"])]

    return None
