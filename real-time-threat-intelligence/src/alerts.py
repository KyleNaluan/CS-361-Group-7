import os
import smtplib
from email.mime.text import MIMEText
import psycopg2
from dotenv import load_dotenv

# Load environment variables from OSINT.env
load_dotenv("OSINT.env")

def send_alert(threat_name, risk_score):
    if risk_score <= 20:
        return

    message = MIMEText(f"High-Risk Threat Detected: {threat_name} with Risk Score {risk_score}")
    message["Subject"] = "Critical Cybersecurity Alert"
    message["From"] = os.getenv("ALERT_EMAIL_FROM")
    message["To"] = os.getenv("ALERT_EMAIL_TO")

    try:
        with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
            server.starttls()
            server.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
            server.sendmail(message["From"], message["To"], message.as_string())
        print("Alert email sent.")
    except Exception as e:
        print(f"Failed to send alert: {e}")

def check_and_alert():
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
            SELECT t.name, r.risk_score
            FROM schema.risk_assessments r
            JOIN schema.threats t ON r.threat_id = t.id
            WHERE r.risk_score > 20
        """)
        results = cursor.fetchall()
        for threat_name, risk_score in results:
            send_alert(threat_name, risk_score)

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database connection error: {e}")

if __name__ == "__main__":
    check_and_alert()
