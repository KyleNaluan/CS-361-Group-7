"""
This script fetches threat intelligence data from the Shodan API for a given IP address
and stores the results (open ports and hostnames) into the PostgreSQL database under
schema.threat_data. This file satisfies Week 4 Task 1 for CS-361.
"""

import os
import json
import requests
import psycopg2
from dotenv import load_dotenv

# Load environment variables from OSINT.env (API key, DB config)
load_dotenv("OSINT.env")

def fetch_shodan_data(ip="8.8.8.8"):
    # Build the request URL for Shodan API
    api_key = os.getenv("SHODAN_API_KEY")
    url = f"https://api.shodan.io/shodan/host/{ip}?key={api_key}"

    try:
        # Send API request
        response = requests.get(url)
        data = response.json()

        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()

        # Insert IP address, open ports, and hostnames into threat_data table
        cursor.execute("""
            INSERT INTO schema.threat_data (ip_address, ports, services)
            VALUES (%s, %s, %s)
        """, (
            ip,
            json.dumps(data.get('ports', [])),
            json.dumps(data.get('hostnames', []))
        ))

        # Commit and clean up
        conn.commit()
        cursor.close()
        conn.close()

        print(f"[Shodan] Data for {ip} saved to database.")
        return data

    except Exception as e:
        print(f"[Shodan] Error: {e}")
        return {}

# Allow user to enter an IP manually for quick lookups during CTF or analysis
if __name__ == "__main__":
    user_ip = input("Enter IP address to scan with Shodan: ").strip()
    fetch_shodan_data(user_ip)