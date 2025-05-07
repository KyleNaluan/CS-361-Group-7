import os
import json
import requests
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv("OSINT.env")

def fetch_shodan_data(ip="8.8.8.8"):
    api_key = os.getenv("SHODAN_API_KEY")
    url = f"https://api.shodan.io/shodan/host/{ip}?key={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        ports = data.get("ports", [])
        services = data.get("hostnames", [])

        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO public.threat_data (ip_address, ports, services)
            VALUES (%s, %s, %s)
        """, (
            ip,
            json.dumps(ports),
            json.dumps(services)
        ))

        conn.commit()
        cursor.close()
        conn.close()

        print(f"✅ Shodan data saved for IP: {ip}")
        return data

    except Exception as e:
        print(f"❌ Shodan Error: {e}")
        return {}

if __name__ == "__main__":
    user_ip = input("Enter IP address to scan with Shodan: ").strip()
    fetch_shodan_data(user_ip)
