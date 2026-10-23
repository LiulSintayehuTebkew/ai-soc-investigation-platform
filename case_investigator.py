import os
import sys

from investigation_prompt import build_case_prompt

ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ollama_service import analyze_text


def investigate_case(
    alert,
    uploaded_events
):
    """
    Correlate Splunk alert + uploaded evidence
    and send everything to Ollama.
    """

    prompt = build_case_prompt(
        alert,
        uploaded_events
    )

    return analyze_text(
        prompt
    )