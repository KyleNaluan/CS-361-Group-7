import smtplib
import psycopg2
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load environment variables from OSINT.env
load_dotenv("OSINT.env")

# Function to send an email alert for high-risk threats
def send_email_alert(threat_name, risk_score):
    if risk_score <= 20:  # Skip if the risk score is not above 20
        return

    # Compose the email message
    message = MIMEText(f"High-Risk Threat Detected: {threat_name} with Risk Score {risk_score}")
    message["Subject"] = "Critical Cybersecurity Alert"
    message["From"] = os.getenv("ALERT_EMAIL_FROM")
    message["To"] = os.getenv("ALERT_EMAIL_TO")

    try:
        # Send the email using SMTP
        with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
            server.starttls()
            server.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
            server.sendmail(message["From"], message["To"], message.as_string())
        print("Alert email sent.")
    except Exception as e:
        print(f"Failed to send alert: {e}")

# Function to check the database for threats with a risk score above 20
def check_and_alert():
    try:
        # Database connection
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()

        # Query to fetch threats with a risk_score > 20 from the appropriate table
        cursor.execute("""
            SELECT threat_type, risk_score
            FROM tva_mapping.threat_intel_temp
            WHERE risk_score > 20
        """)
        results = cursor.fetchall()

        # Loop through the results and send alerts for each high-risk threat
        for threat_name, risk_score in results:
            send_email_alert(threat_name, risk_score)

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database connection error: {e}")

# Run the alert check and email notifications
if __name__ == "__main__":
    check_and_alert()
