import psycopg2

def insert_sample_assets():
    conn = psycopg2.connect(
        dbname="threat_intel",
        user="postgres",
        password="newpassword",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    assets = [
        ("Web Server", "Hardware", "Nginx server hosting e-commerce site"),
        ("Database Server", "Hardware", "PostgreSQL DB storing user info"),
        ("Login Module", "Software", "Handles user authentication"),
        ("User Data", "Data", "Stored credentials and PII"),
        ("System Admin", "People", "Manages internal systems")
    ]

    for asset in assets:
        cursor.execute("""
            INSERT INTO assets (asset_name, asset_type, description)
            VALUES (%s, %s, %s);
        """, asset)

    conn.commit()
    print("✅ Sample assets inserted.")
    cursor.close()
    conn.close()

insert_sample_assets()
