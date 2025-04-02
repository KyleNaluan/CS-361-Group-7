# /src/incident_response.py

def get_incident_response(threat_name):

    threat_name = threat_name.strip().lower()

    response_playbooks = {
        "sql injection": {
            "priority": "High",
            "steps": [
                "Block malicious IP via firewall.",
                "Check for unauthorized DB access or changes.",
                "Apply input sanitization and parameterized queries.",
                "Enable Web Application Firewall (WAF).",
                "Audit and patch vulnerable code.",
            ]
        },
        "phishing": {
            "priority": "High",
            "steps": [
                "Alert affected users and force password resets.",
                "Search inboxes for similar malicious emails.",
                "Block sender's domain/IP.",
                "Review email filters and spam controls.",
                "Provide phishing awareness training.",
            ]
        },
        "ddos": {
            "priority": "Medium",
            "steps": [
                "Activate DDoS mitigation (e.g., Cloudflare, AWS Shield).",
                "Rate-limit or block attacker IPs.",
                "Notify ISP or cloud provider.",
                "Scale infrastructure if needed.",
                "Analyze traffic patterns for source.",
            ]
        },
        "ransomware": {
            "priority": "Critical",
            "steps": [
                "Isolate affected machines from the network.",
                "Disable shared drives and services.",
                "Initiate recovery from secure backups.",
                "Notify incident response and legal teams.",
                "Preserve evidence and report to law enforcement.",
            ]
        },
        "unauthorized access": {
            "priority": "High",
            "steps": [
                "Revoke compromised credentials.",
                "Audit access logs and unusual activity.",
                "Force MFA enrollment for affected users.",
                "Check for data exfiltration.",
                "Update permissions and conduct policy review.",
            ]
        }
    }

    return response_playbooks.get(threat_name, {
        "priority": "Low",
        "steps": ["No predefined response plan available for this threat."]
    })