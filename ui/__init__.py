"""UI package. Public API is unchanged: `from ui import render_sidebar, ...`"""
from .sidebar import render_sidebar
from .alerts import render_metrics, render_alert_table
from .investigation import render_analysis

__all__ = ["render_sidebar", "render_metrics", "render_alert_table", "render_analysis"]
