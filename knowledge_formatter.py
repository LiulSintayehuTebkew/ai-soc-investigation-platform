def build_case_document(
        alert,
        analysis,
        verdict
):

    return f"""
Attack Summary

Alert:
{alert.get('title')}

Source:
{alert.get('ip')}

User:
{alert.get('user')}

Analysis:
{analysis}

Verdict:
{verdict}

Lessons Learned:
- Investigation completed
- Pattern stored for future retrieval
"""