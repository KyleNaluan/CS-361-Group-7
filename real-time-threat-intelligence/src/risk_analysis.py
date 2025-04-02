import os
import openai
import psycopg2
from dotenv import load_dotenv

# Load API keys and DB config
load_dotenv("OSINT.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_risk(threat_name, likelihood, impact):
    prompt = (
        f"Given the threat '{threat_name}', with likelihood {likelihood} and impact {impact}, "
        "calculate a risk score from 1 to 25 and explain why."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a cybersecurity assistant scoring threats."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"AI error: {e}"

def insert_risk_score(asset_id, threat_id, likelihood, impact, risk_score, notes):
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
            INSERT INTO schema.risk_assessments (
                asset_id, threat_id, likelihood, impact, risk_score,
                risk_level, assessment_date, created_at, updated_at, notes
            ) VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE, NOW(), NOW(), %s)
        """, (
            asset_id, threat_id, likelihood, impact, risk_score,
            "High" if risk_score > 20 else "Medium",
            notes
        ))
        conn.commit()
        cursor.close()
        conn.close()
        print("Risk score inserted into database.")
    except Exception as e:
        print(f"Database insertion error: {e}")

# Example execution
if __name__ == "__main__":
    threat = "SQL Injection"
    likelihood = 4
    impact = 5

    ai_result = analyze_risk(threat, likelihood, impact)
    print("AI Response:\n", ai_result)

    # Placeholder score for demonstration (you could parse this from ai_result)
    insert_risk_score(
        asset_id=1,
        threat_id=1,
        likelihood=likelihood,
        impact=impact,
        risk_score=22,
        notes=ai_result
    )
