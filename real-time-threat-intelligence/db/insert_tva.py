import psycopg2


def insert_sample_tva():
    conn = psycopg2.connect(
        dbname="threat_intel",
        user="postgres",
        password="newpassword",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    tva_entries = [
        (1, "SQL Injection", "Improperly sanitized input field", 5, 5),
        (2, "Open Port Exposure", "Unrestricted access to DB port", 4, 4),
        (3, "Credential Stuffing", "Weak password reuse by users", 3, 4),
        (4, "Data Breach Risk", "PII storage not encrypted", 4, 5),
        (5, "Social Engineering", "No MFA for admin accounts", 3, 5)
    ]

    for entry in tva_entries:
        cursor.execute("""
            INSERT INTO tva_mapping (asset_id, threat_name, vulnerability_description, likelihood, impact)
            VALUES (%s, %s, %s, %s, %s);
        """, entry)

    conn.commit()
    print("✅ Sample TVA mappings inserted.")
    cursor.close()
    conn.close()

insert_sample_tva()
