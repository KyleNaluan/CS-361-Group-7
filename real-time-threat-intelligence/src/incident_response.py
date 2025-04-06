import psycopg2
import datetime

def get_incident_response(threat_name):

    threat_name = threat_name.strip().lower()

    response_playbooks = {
        "sql injection": {
            "priority": "High",
            "nist_phases": ["Detection & Analysis", "Containment, Eradication, & Recovery"],
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
            "nist_phases": ["Detection & Analysis", "Post-Incident Activity"],
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
            "nist_phases": ["Containment, Eradication, & Recovery"],
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
            "nist_phases": ["Detection & Analysis", "Containment, Eradication, & Recovery", "Post-Incident Activity"],
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
            "nist_phases": ["Detection & Analysis", "Containment, Eradication, & Recovery", "Post-Incident Activity"],
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
        "nist_phases": ["Preparation"],
        "steps": ["No predefined response plan available for this threat."]
    })

# Database connection settings
DB_CONFIG = {
    "dbname": "threat_intel",
    "user": "admin",
    "password": "CSGroup7",
    "host": "localhost",
    "port": 5432,
}

def log_incident(threat_name, risk_score, response_plan):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO schema.incident_logs (threat_name, risk_score, priority, nist_phases, response_steps, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            threat_name,
            risk_score,
            response_plan["priority"],
            ", ".join(response_plan["nist_phases"]),
            "\n".join(response_plan["steps"]),
            datetime.utcnow()
        ))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"Incident logged for threat: {threat_name}")
    except Exception as e:
        print(f"Error logging incident: {e}")