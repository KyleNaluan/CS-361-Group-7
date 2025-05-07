# src/risk_prioritization.py

import psycopg2
import os
from dotenv import load_dotenv

# Load env variables (adjust the path if needed)
load_dotenv(dotenv_path="../api/OSINT.env")

def calculate_risk_score(vt_score, abuse_score, total_reports):
    """
    Calculate a combined risk score:
      - vt_score: VirusTotal 'community' reputation (can be negative)
      - abuse_score: AbuseIPDB confidence (0–100)
      - total_reports: number of reports (capped at 100)
    Any negative vt_score is flipped to positive risk via abs().
    Weights: 40% VT, 40% Abuse, 20% Reports.
    """
    # Flip negative community scores into positive risk
    vt_risk = abs(vt_score)

    # Cap total_reports to 100 to avoid extreme skew
    total_reports = min(total_reports, 100)

    # Weighted average
    combined = (vt_risk * 0.4) + (abuse_score * 0.4) + (total_reports * 0.2)
    return round(combined, 2)

def prioritize_risks(threats):
    """
    Given a list of threats (each with a 'risk_score' key),
    return them sorted descending by risk_score.
    """
    return sorted(threats, key=lambda x: x["risk_score"], reverse=True)

def fetch_real_threats():
    """
    Pulls raw threat data from the DB, computes risk scores,
    and returns a prioritized list.
    """
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT ip_address, vt_score, abuse_score, total_reports
            FROM threat_data
            WHERE vt_score IS NOT NULL
              AND abuse_score IS NOT NULL
              AND total_reports IS NOT NULL
        """)
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    threats = []
    for ip, vt, abuse, reports in rows:
        score = calculate_risk_score(vt, abuse, reports)
        threats.append({
            "ip": ip,
            "vt_score": vt,
            "abuse_score": abuse,
            "total_reports": reports,
            "risk_score": score
        })

    return prioritize_risks(threats)

if __name__ == "__main__":
    print("🔍 Fetching and prioritizing threats...\n")
    threats = fetch_real_threats()
    if threats:
        print("🔥 Top Threats by Risk Score:")
        for t in threats:
            print(f"IP: {t['ip']} — Score: {t['risk_score']}")
    else:
        print("⚠️ No valid threats found.")
