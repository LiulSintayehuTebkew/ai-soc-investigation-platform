def correlate_events(events):

    findings = []

    ip_map = {}
    user_map = {}

    for event in events:

        ip = (
            event.get("src_ip")
            or event.get(
                "Source_Network_Address"
            )
        )

        user = (
            event.get("user")
            or event.get(
                "Account_Name"
            )
        )

        if ip:

            ip_map.setdefault(
                ip,
                []
            ).append(event)

        if user:

            user_map.setdefault(
                user,
                []
            ).append(event)

    for ip, group in ip_map.items():

        if len(group) > 1:

            findings.append(
                f"{len(group)} events share IP {ip}"
            )

    for user, group in user_map.items():

        if len(group) > 1:

            findings.append(
                f"{len(group)} events share user {user}"
            )

    return findings