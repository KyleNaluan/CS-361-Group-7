import psycopg2

def connect_and_test():
    try:
        conn = psycopg2.connect(
            dbname="threat_intel",
            user="postgres",
            password="newpassword",  # <- put the one you reset earlier
            host="localhost",
            port="5432"
        )

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM assets;")
        rows = cursor.fetchall()

        print("Data from assets table:")
        for row in rows:
            print(row)

        cursor.close()
        conn.close()

    except Exception as e:
        print("Failed to connect or query:", e)

# Run the test
connect_and_test()
