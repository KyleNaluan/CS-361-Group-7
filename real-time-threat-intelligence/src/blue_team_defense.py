import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Load environment variables from .env file
load_dotenv("../api/OSINT.env")

# Database connection setup
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

# Initialize Flask app
app = Flask(__name__)

# Function to block an IP based on threat intelligence
def block_ip(ip):
    os.system(f"iptables -A INPUT -s {ip} -j DROP")
    print(f"Blocked IP: {ip}")

# Fetch malicious IPs from the database and block them
def block_malicious_ips():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Query to fetch malicious IPs (e.g., those with a high abuse score)
        cursor.execute("""
            SELECT ip_address
            FROM threat_data
            WHERE abuse_score > 80
        """)

        malicious_ips = cursor.fetchall()

        for ip in malicious_ips:
            block_ip(ip[0])

        cursor.close()
        conn.close()

        return "Malicious IPs blocked successfully."

    except Exception as e:
        return f"Error fetching or blocking IPs: {e}"

@app.route("/api/block_malicious_ips", methods=["POST"])
def block_malicious_ips_endpoint():
    response = block_malicious_ips()
    return jsonify({"message": response})

if __name__ == "__main__":
    app.run(debug=True)
