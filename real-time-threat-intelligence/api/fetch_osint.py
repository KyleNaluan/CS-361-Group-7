import os
import time
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

import sys
sys.path.append(os.path.abspath("../src"))  # Or remove if you've moved risk_prioritization.py into api/
from risk_prioritization import calculate_risk_score

from virustotal import virustotal_get_ip_report
from abuseipdb import abuseipdb_check_ip

# Load environment variables
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "OSINT.env"))
load_dotenv(dotenv_path)

# API Keys
vt_api_key = os.getenv("VIRUSTOTAL_API_KEY")
abuseipdb_api_key = os.getenv("ABUSEIPDB_API_KEY")

# Prompt for target IP
ip = input("🔍 Enter an IP address to scan (e.g., 185.232.67.173): ").strip()

def run_threat_fetch():
    print(f"\n🕒 Fetching threat data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Fetch threat data from APIs
    vt_data = virustotal_get_ip_report(ip, vt_api_key)
    abuse_data = abuseipdb_check_ip(ip, abuseipdb_api_key)

    if not vt_data or not abuse_data:
        if not vt_data:
            print("❌ VirusTotal API failed.")
        if not abuse_data:
            print("❌ AbuseIPDB API failed.")
        print("⚠️ Skipping this run due to missing data.\n")
        return

    # Debug: show entire VT response
    print("🔍 Full VirusTotal response:")
    print(vt_data)

    # Extract VT reputation (allow negatives)
    vt_rep = vt_data.get("reputation", 0)
    # **DO NOT** zero-out negatives here — let risk_prioritization.flip them later

    abuse_conf = abuse_data.get("abuseConfidenceScore", 0)
    abuse_reports = abuse_data.get("totalReports", 0)

    # Debug: print parsed values
    print(f"▶️ Parsed VirusTotal reputation: {vt_rep}")
    print(f"▶️ Parsed AbuseIPDB confidence: {abuse_conf}")
    print(f"▶️ Parsed AbuseIPDB total reports: {abuse_reports}")

    # Scale confidence from 0–100 to 0–10
    confidence_score = round(abuse_conf / 10)
    confidence_score = max(1, confidence_score) if abuse_conf > 0 else 0

    # Final risk score calculation
    risk_score = calculate_risk_score(vt_rep, abuse_conf, abuse_reports)
    print(f"▶️ Calculated risk_score: {risk_score}")

    # Insert into DB
    try:
        conn = psycopg2.connect(
            dbname="threat_intel",
            user="postgres",
            password="newpassword",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        print("📥 Inserting threat data into threat_intel_temp...")
        cursor.execute("""
            INSERT INTO tva_mapping.threat_intel_temp (
                threat_type, risk_score, confidence, last_observed,
                source, details, ip_address
            ) VALUES (%s, %s, %s, NOW(), %s, %s, %s)
        """, (
            "Malicious IP Detected",
            risk_score,
            confidence_score,
            "VirusTotal + AbuseIPDB",
            f"VT rep: {vt_rep}, reports: {abuse_reports}",
            ip
        ))

        conn.commit()
        print("✅ Threat data saved.")
    except Exception as e:
        print("❌ Error inserting threat data:", e)
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    run_threat_fetch()
