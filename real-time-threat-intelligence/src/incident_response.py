import psycopg2
import datetime
import os
from dotenv import load_dotenv
from mitigation_recommendations import recommend_mitigation

# Load DB credentials from .env
load_dotenv(dotenv_path="../api/osint.env")

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

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
        },
        "malicious ip detected": {  # Added specific response for malicious IP
            "priority": "Medium",
            "nist_phases": ["Detection & Analysis", "Containment, Eradication, & Recovery"],
            "steps": [
                "Block the malicious IP via firewall.",
                "Check logs for any suspicious activities linked to the IP.",
                "Report the malicious IP to threat intelligence databases.",
                "Monitor network traffic for any further signs of attack.",
                "Implement rate limiting for repeated failed login attempts.",
            ]
        }
    }

    return response_playbooks.get(threat_name, {
        "priority": "Low",
        "nist_phases": ["Preparation"],
        "steps": ["No predefined response plan available for this threat."]
    })

def build_incident_response(threat_name, risk_score):
    plan = get_incident_response(threat_name)
    plan["mitigation"] = recommend_mitigation(threat_name)
    plan["risk_score"] = risk_score
    plan["threat_name"] = threat_name
    return plan

def log_incident(threat_name, risk_score, response_plan):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute(""" 
            INSERT INTO public.incident_logs (threat_name, risk_score, priority, nist_phases, response_steps, mitigation, timestamp) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            threat_name,
            risk_score,
            response_plan["priority"],
            response_plan["nist_phases"],
            response_plan["steps"],
            response_plan["mitigation"],
            datetime.datetime.utcnow()
        ))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Incident logged for: {threat_name}")

    except Exception as e:
        print(f"❌ Error logging incident: {e}")

# Function to fetch threats with a risk score greater than 20 from the database and log incidents
def log_incidents_from_database():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute(""" 
            SELECT threat_name, risk_score 
            FROM public.risk_assessments 
            WHERE risk_score > 20
        """)

        rows = cursor.fetchall()
        for row in rows:
            threat_name, risk_score = row
            response_plan = build_incident_response(threat_name, risk_score)
            log_incident(threat_name, risk_score, response_plan)

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error fetching data from database: {e}")

# Run the function to log incidents from the database
if __name__ == "__main__":
    log_incidents_from_database()
