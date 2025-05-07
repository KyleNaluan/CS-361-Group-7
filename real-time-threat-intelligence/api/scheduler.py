"""
Scheduler Script for Week 4 Task 2 - CS-361 Project
Fetches OSINT threat intelligence data every 6 hours using:
- Shodan
- VirusTotal
- AbuseIPDB
- SecurityTrails
Saves data to PostgreSQL and triggers email alerts for high-risk threats.
"""

import os
import time
import schedule
import psycopg2
import importlib.util
from dotenv import load_dotenv
from alerts import send_email_alert

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "api", "OSINT.env"))

# === Dynamic Import Utility ===
def import_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
shodan_integration = import_from_file("shodan_integration", os.path.join(base_dir, "shodun_integration.py"))
allosint = import_from_file("allosint", os.path.join(base_dir, "ALLOSINT.py"))

# Alert Threshold
ALERT_THRESHOLD = 20

# Get IPs from threat_data
def get_ips_from_threat_logs():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT ip_address FROM public.threat_data")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [r[0] for r in rows if r[0]]
    except Exception as e:
        print(f"[Scheduler] ❌ Failed to fetch IPs from threat_data: {e}")
        return []

# === OSINT Check Loop ===
def run_osint_updates():
    ip_list = get_ips_from_threat_logs()
    for ip in ip_list:
        print(f"[Scheduler] 🔍 Running OSINT checks for {ip}...")

        shodan_integration.fetch_shodan_data(ip)
        vt_data = allosint.virustotal_get_ip_report(ip, os.getenv("VIRUSTOTAL_API_KEY"))
        abuse_data = allosint.abuseipdb_check_ip(ip, os.getenv("ABUSEIPDB_API_KEY"))
        st_data = allosint.query_securitytrails("example.com", os.getenv("SECURITYTRAILS_API_KEY"))

        vt_score = vt_data.get("reputation") if vt_data else 0
        abuse_score = abuse_data.get("abuseConfidenceScore") if abuse_data else 0
        total_reports = abuse_data.get("totalReports") if abuse_data else 0

        combined_risk = vt_score + abuse_score

        try:
            conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO public.osint_logs (
                    ip, vt_reputation, abuse_score, total_reports,
                    domain, created_date, registrar
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                ip,
                vt_score,
                abuse_score,
                total_reports,
                "example.com",
                st_data.get("createdDate") if st_data else None,
                st_data.get("registrar") if st_data else None
            ))

            conn.commit()
            cursor.close()
            conn.close()

            print(f"[Scheduler] ✅ OSINT logs saved for {ip}.")

            # Alert if above threshold
            if combined_risk > ALERT_THRESHOLD:
                send_email_alert("Malicious IP Detected", combined_risk, ip)

        except Exception as e:
            print(f"[Scheduler] ❌ DB insert error for {ip}: {e}")

    print("[Scheduler] 🕑 Will re-scan in 6 hours.\n")

# === Schedule ===
schedule.every(6).hours.do(run_osint_updates)

if __name__ == "__main__":
    print("[Scheduler] 🔁 Starting OSINT update loop...")
    run_osint_updates()
    while True:
        schedule.run_pending()
        time.sleep(1)
