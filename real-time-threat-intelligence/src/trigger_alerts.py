import psycopg2

def trigger_risk_alerts():
    conn = psycopg2.connect(
        dbname="threat_intel",
        user="postgres",
        password="newpassword",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Step 1: Get all high-risk mappings (score >= 20)
    cursor.execute("""
        SELECT id, threat_name, risk_score
        FROM tva_mapping
        WHERE risk_score >= 20;
    """)
    high_risks = cursor.fetchall()

    # Step 2: Insert alerts into logs
    for threat_id, threat_name, risk_score in high_risks:
        alert_msg = f"⚠️ High-Risk Alert: {threat_name} (Score: {risk_score})"
        cursor.execute("""
            INSERT INTO logs (event_type, description)
            VALUES (%s, %s);
        """, ("High Risk Alert", alert_msg))
        print(alert_msg)

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Alerts logged for high-risk threats.")

trigger_risk_alerts()
