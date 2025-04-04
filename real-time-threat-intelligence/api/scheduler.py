"""
This scheduler runs a full OSINT fetch every 6 hours as part of Week 4 Task 2.
It calls multiple APIs (Shodan, VirusTotal, AbuseIPDB, SecurityTrails) and stores
results in the appropriate PostgreSQL tables. IPs are listed in this file for now.
"""

import schedule
import time
from shodan_integration import fetch_shodan_data
from ALLOSINT import virustotal_get_ip_report, abuseipdb_check_ip, query_securitytrails
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv("OSINT.env")

# IPs to scan - manually updated or pulled from logs in future use
ip_list = [
    "8.8.8.8",
    "1.1.1.1",
    "203.0.113.42"
]

def run_osint_updates():
    for ip in ip_list:
        print(f"[Scheduler] Running OSINT checks for {ip}...")

        # Fetch and store Shodan data
        fetch_shodan_data(ip)

        # Fetch other API data
        vt_data = virustotal_get_ip_report(ip, os.getenv("VIRUSTOTAL_API_KEY"))
        abuse_data = abuseipdb_check_ip(ip, os.getenv("ABUSEIPDB_API_KEY"))
        st_data = query_securitytrails("example.com", os.getenv("SECURITYTRAILS_API_KEY"))

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
                INSERT INTO schema.osint_logs (
                    ip, vt_reputation, abuse_score, total_reports,
                    domain, created_date, registrar
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                ip,
                vt_data.get("reputation"),
                abuse_data.get("abuseConfidenceScore"),
                abuse_data.get("totalReports"),
                "example.com",
                st_data.get("createdDate"),
                st_data.get("registrar")
            ))

            conn.commit()
            cursor.close()
            conn.close()
            print(f"[Scheduler] Data saved for {ip} into osint_logs table.\n")

        except Exception as e:
            print(f"[Scheduler] DB insert error for {ip}: {e}")

# Schedule to run every 6 hours
schedule.every(6).hours.do(run_osint_updates)

if __name__ == "__main__":
    print("[Scheduler] Starting full OSINT job loop.")
    run_osint_updates()
    while True:
        schedule.run_pending()
        time.sleep(1)
