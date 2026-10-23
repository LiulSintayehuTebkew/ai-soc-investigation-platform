import json


def build_case_prompt(
    alert,
    uploaded_events
):

    return f"""
You are a Senior SOC Analyst.

Analyze ALL evidence together.

Determine:

1. Are the events related?
2. What attack chain is occurring?
3. Timeline of attacker activity
4. MITRE ATT&CK mapping
5. Indicators of Compromise
6. Severity
7. Recommended Actions

Primary Splunk Alert:

{json.dumps(alert, indent=2)}

Additional Uploaded Logs:

{json.dumps(uploaded_events, indent=2)}

Provide ONE consolidated investigation report.
"""