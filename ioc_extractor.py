import re


def extract_iocs(alert):

    text = str(alert)

    ips = list(set(
        re.findall(
            r'(?:\d{1,3}\.){3}\d{1,3}',
            text
        )
    ))

    domains = list(set(
        re.findall(
            r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b',
            text
        )
    ))

    md5 = list(set(
        re.findall(
            r'\b[a-fA-F0-9]{32}\b',
            text
        )
    ))

    sha1 = list(set(
        re.findall(
            r'\b[a-fA-F0-9]{40}\b',
            text
        )
    ))

    sha256 = list(set(
        re.findall(
            r'\b[a-fA-F0-9]{64}\b',
            text
        )
    ))

    users = []

    raw_alert = alert.get("alert", {})

    # Your normalized format
    user = raw_alert.get("user")

    if user:
        users.append(str(user))

    host = (
        raw_alert.get("host")
        or raw_alert.get("Workstation_Name")
        or "N/A"
    )

    return {
        "ips": ips,
        "domains": domains,
        "users": users,
        "host": host,
        "md5": md5,
        "sha1": sha1,
        "sha256": sha256
    }