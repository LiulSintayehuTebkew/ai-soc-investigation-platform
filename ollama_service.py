import json
import requests

from rag_context import get_rag_context


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"


# ==================================================
# LOW LEVEL OLLAMA REQUEST
# ==================================================

def analyze_text(prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )

    response.raise_for_status()

    return response.json()["response"]


# ==================================================
# RAG CONTEXT
# ==================================================

def format_historical_context(alert):

    try:

        context = get_rag_context(alert)

        confirmed_cases = context.get(
            "confirmed",
            []
        )

        false_positive_cases = context.get(
            "false_positive",
            []
        )

        confirmed_text = "\n\n".join(
            confirmed_cases
        ) if confirmed_cases else "No similar confirmed attacks found."

        false_positive_text = "\n\n".join(
            false_positive_cases
        ) if false_positive_cases else "No similar false positives found."

        return (
            confirmed_text,
            false_positive_text
        )

    except Exception:

        return (
            "No historical attack data available.",
            "No historical false-positive data available."
        )


# ==================================================
# SINGLE ALERT ANALYSIS
# ==================================================

def analyze_alert(alert):

    confirmed_text, false_positive_text = (
        format_historical_context(alert)
    )

    prompt = f"""
You are a Senior SOC Analyst.

You have access to analyst-reviewed historical cases.

You MUST use historical investigations
when determining severity and confidence.

==================================================
HISTORICAL CONFIRMED ATTACKS
==================================================

{confirmed_text}

==================================================
HISTORICAL FALSE POSITIVES
==================================================

{false_positive_text}

==================================================
CURRENT SECURITY EVENT
==================================================

{json.dumps(alert, indent=2)}

==================================================
INSTRUCTIONS
==================================================

Review the historical investigations first.

If similar cases exist:

- cite them explicitly
- explain similarities
- explain differences
- explain how analyst feedback affects your assessment

Always include an Organizational Knowledge section.

Respond ONLY in the following format.


## Severity

Low / Medium / High / Critical


## Confidence

0-100


## Organizational Knowledge

Include:

- Similar confirmed attacks
- Similar false positives
- Historical lessons learned
- Analyst feedback impact
- Why the current case resembles or differs
  from previous investigations


## Summary

Provide:

- What happened
- Why it is suspicious
- MITRE ATT&CK Technique ID
- MITRE ATT&CK Technique Name
- MITRE ATT&CK Tactic


## Indicators of Compromise

List:

- Users
- Source IPs
- Hosts
- Domains
- Hashes


## Recommended Actions

Provide practical SOC analyst recommendations.
"""

    return analyze_text(prompt)


# ==================================================
# MULTI SOURCE CASE INVESTIGATION
# ==================================================

def analyze_case(
    primary_alert,
    uploaded_events
):

    confirmed_text, false_positive_text = (
        format_historical_context(primary_alert)
    )

    prompt = f"""
You are a Senior SOC Analyst.

You have access to historical, analyst-confirmed
organizational investigations.

==================================================
HISTORICAL CONFIRMED ATTACKS
==================================================

{confirmed_text}

==================================================
HISTORICAL FALSE POSITIVES
==================================================

{false_positive_text}

==================================================
PRIMARY ALERT
==================================================

{json.dumps(primary_alert, indent=2)}

==================================================
UPLOADED EVIDENCE
==================================================

{json.dumps(uploaded_events, indent=2)}

==================================================
INVESTIGATION GOALS
==================================================

Analyze ALL evidence together.

Determine:

1. Whether events are related
2. Potential attack chain
3. Timeline of activity
4. MITRE ATT&CK mapping
5. Indicators of Compromise
6. Affected assets
7. Incident severity
8. Recommended response actions

You MUST explain how historical analyst
feedback influenced your conclusions.

Respond ONLY in the following format.


## Severity


## Confidence


## Organizational Knowledge

Include:

- Similar confirmed attacks
- Similar false positives
- Historical lessons learned
- Analyst feedback impact
- Similarities to previous investigations


## Executive Summary


## Timeline


## MITRE ATT&CK Mapping


## Indicators of Compromise


## Affected Assets


## Recommended Actions


## Final Assessment
"""

    return analyze_text(prompt)


# ==================================================
# KNOWLEDGE EXTRACTION
# ==================================================

def generate_case_lesson(
    alert,
    analysis,
    verdict
):

    prompt = f"""
You are a SOC Knowledge Engineer.

Create a reusable SOC case record.

Alert:

{json.dumps(alert, indent=2)}

Investigation:

{analysis}

Verdict:

{verdict}

Return ONLY the structure below.


Attack Type:

MITRE ATT&CK Techniques:

Key Indicators:

Detection Pattern:

Lessons Learned:

Recommended Response:

False Positive Characteristics:

Analyst Verdict:
"""

    return analyze_text(prompt)