'''
#Code here has working Virustotal & abuseipdp
import os
import psycopg2
from dotenv import load_dotenv

#  Import your API functions
from virustotal import virustotal_get_ip_report
from abuseipdb import abuseipdb_check_ip
from securitytrails import query_securitytrails

#  Load environment variables from .env
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "OSINT.env"))
load_dotenv(dotenv_path)

#  Get API keys from environment
vt_api_key = os.getenv("VIRUSTOTAL_API_KEY")
st_api_key = os.getenv("SECURITYTRAILS_API_KEY")
abuseipdb_api_key = os.getenv("ABUSEIPDB_API_KEY")

#  IP and Domain to query
ip = "8.8.8.8"
domain = "example.com"

#  Fetch threat data
vt_data = virustotal_get_ip_report(ip, vt_api_key)
abuse_data = abuseipdb_check_ip(ip, abuseipdb_api_key)
st_data = query_securitytrails(domain, st_api_key)

#  Connect to PostgreSQL and insert data
try:
    conn = psycopg2.connect(
        dbname="threat_intel",
        user="postgres",            
        password="Pureleaf",   # ←real PostgreSQL password
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    #  Debug print
    print(" Preparing to insert data into threat_data table...")
    print("Insert values:")
    print((
        ip,
        vt_data.get("reputation"),
        abuse_data.get("abuseConfidenceScore"),
        abuse_data.get("totalReports"),
        domain,
        st_data.get("createdDate"),
        st_data.get("registrar")
    ))

    #  Insert into table
    cursor.execute("""
        INSERT INTO threat_data (
            ip, vt_reputation, abuse_score, total_reports,
            domain, created_date, registrar
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        ip,
        vt_data.get("reputation"),
        abuse_data.get("abuseConfidenceScore"),
        abuse_data.get("totalReports"),
        domain,
        st_data.get("createdDate"),
        st_data.get("registrar")
    ))

    conn.commit()
    print(" Threat data successfully stored in database.")

except Exception as e:
    print(" Error inserting into database:")
    raise e

finally:
    if conn:
        cursor.close()
        conn.close()
'''




'''
#New code for updating time, SecurityTrails still fails
import os
import time
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

# Import your API functions
from virustotal import virustotal_get_ip_report
from abuseipdb import abuseipdb_check_ip
from securitytrails import query_securitytrails
from risk_prioritization import calculate_risk_score


# Load environment variables from .env
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "OSINT.env"))
load_dotenv(dotenv_path)

# Get API keys from environment
vt_api_key = os.getenv("VIRUSTOTAL_API_KEY")
st_api_key = os.getenv("SECURITYTRAILS_API_KEY")
abuseipdb_api_key = os.getenv("ABUSEIPDB_API_KEY")

# IP and Domain to query
ip = "8.8.8.8"
domain = "example.com"

# Main threat fetch function
def run_threat_fetch():
    print("\n Fetching threat data at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Fetch threat data
    vt_data = virustotal_get_ip_report(ip, vt_api_key)
    abuse_data = abuseipdb_check_ip(ip, abuseipdb_api_key)
    st_data = query_securitytrails(domain, st_api_key)

    #  Exit early if any API call failed
    if not vt_data or not abuse_data or not st_data:
        if not vt_data:
            print(" VirusTotal API failed.")
        if not abuse_data:
            print(" AbuseIPDB API failed.")
        if not st_data:
            print(" SecurityTrails API failed.")
        print(" Skipping this run due to missing data.\n")
        return

    try:
        conn = psycopg2.connect(
            dbname="threat_intel",
            user="postgres",            
            password="Pureleaf",   # ← PostgreSQL password
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        print(" Preparing to insert data into threat_data table...")
        print("Insert values:")
        print((
            ip,
            vt_data.get("reputation"),
            abuse_data.get("abuseConfidenceScore"),
            abuse_data.get("totalReports"),
            domain,
            st_data.get("createdDate"),
            st_data.get("registrar")
        ))

        # Insert into table
        cursor.execute("""
            INSERT INTO threat_data (
                ip, vt_reputation, abuse_score, total_reports,
                domain, created_date, registrar
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            ip,
            vt_data.get("reputation"),
            abuse_data.get("abuseConfidenceScore"),
            abuse_data.get("totalReports"),
            domain,
            st_data.get("createdDate"),
            st_data.get("registrar")
        
        ))

        conn.commit()
        print(" Threat data successfully stored in database.")

    except Exception as e:
        print(" Error inserting into database:")
        raise e

    finally:
        if conn:
            cursor.close()
            conn.close()

#  Run the fetch every 8 hours forever
while True:
    run_threat_fetch()
    print(" Waiting 8 hours for the next update...\n")
    time.sleep(8 * 60 * 60)  # 8 hours = 28,800 seconds
'''

import os
import time
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

from virustotal import virustotal_get_ip_report
from abuseipdb import abuseipdb_check_ip
from securitytrails import query_securitytrails
from risk_prioritization import calculate_risk_score

# Load environment variables from .env
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "OSINT.env"))
load_dotenv(dotenv_path)

# Get API keys from environment
vt_api_key = os.getenv("VIRUSTOTAL_API_KEY")
st_api_key = os.getenv("SECURITYTRAILS_API_KEY")
abuseipdb_api_key = os.getenv("ABUSEIPDB_API_KEY")

# IP and Domain to query
ip = "8.8.8.8"
domain = "example.com"

def run_threat_fetch():
    print("\n Fetching threat data at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Fetch threat data
    vt_data = virustotal_get_ip_report(ip, vt_api_key)
    abuse_data = abuseipdb_check_ip(ip, abuseipdb_api_key)
    st_data = query_securitytrails(domain, st_api_key)

    # Exit early if any API failed
    if not vt_data or not abuse_data or not st_data:
        if not vt_data:
            print(" VirusTotal API failed.")
        if not abuse_data:
            print(" AbuseIPDB API failed.")
        if not st_data:
            print(" SecurityTrails API failed.")
        print(" Skipping this run due to missing data.\n")
        return

    #  Calculate risk score
    risk_score = calculate_risk_score(
        vt_data.get("reputation", 0),
        abuse_data.get("abuseConfidenceScore", 0),
        abuse_data.get("totalReports", 0)
    )

    print(" Calculated Risk Score:", risk_score)
    if risk_score >= 70:
        print(" Immediate threat detected!")

    try:
        conn = psycopg2.connect(
            dbname="threat_intel",
            user="postgres",            
            password="Pureleaf",   
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        print("🛠 Preparing to insert data into threat_data table...")
        print("Insert values:")
        print((
            ip,
            vt_data.get("reputation"),
            abuse_data.get("abuseConfidenceScore"),
            abuse_data.get("totalReports"),
            domain,
            st_data.get("createdDate"),
            st_data.get("registrar"),
            risk_score
        ))

        cursor.execute("""
            INSERT INTO threat_data (
                ip, vt_reputation, abuse_score, total_reports,
                domain, created_date, registrar, risk_score
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            ip,
            vt_data.get("reputation"),
            abuse_data.get("abuseConfidenceScore"),
            abuse_data.get("totalReports"),
            domain,
            st_data.get("createdDate"),
            st_data.get("registrar"),
            risk_score
        ))

        conn.commit()
        print(" Threat data successfully stored in database.")

    except Exception as e:
        print(" Error inserting into database:")
        raise e

    finally:
        if conn:
            cursor.close()
            conn.close()

#  Loop: Run every 8 hours
while True:
    run_threat_fetch()
    print(" Waiting 8 hours for the next update...\n")
    time.sleep(8 * 60 * 60)  # 8 hours in seconds
