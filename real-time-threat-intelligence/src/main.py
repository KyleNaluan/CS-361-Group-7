import psycopg2
from flask import Flask, jsonify
from flask_cors import CORS
from incident_response import build_incident_response

app = Flask(__name__)
CORS(app)

# Database Config
DB_CONFIG = {
    "dbname": "threat_intel",
    "user": "postgres",
    "password": "newpassword",  # Change if needed
    "host": "localhost",
    "port": "5432"
}

# ✅ 1. Asset Inventory API
@app.route("/api/assets")
def get_assets():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(""" 
            SELECT asset_name, asset_type, description 
            FROM assets.assets 
        """)
        rows = cursor.fetchall()
        data = [{"name": r[0], "type": r[1], "description": r[2]} for r in rows]
        return jsonify(data)
    except Exception as e:
        print(f"❌ DB error (assets): {e}")
        return jsonify({"error": "Failed to fetch assets"}), 500
    finally:
        cursor.close()
        conn.close()

# ✅ 2. TVA Mapping API
@app.route("/api/tva-mapping")
def get_tva_mapping():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(""" 
            SELECT asset_name, threat_name, vulnerability_description,
                   likelihood, impact, risk_score, risk_level 
            FROM tva_mapping.tva_intel_view 
        """)
        rows = cursor.fetchall()
        data = []
        for r in rows:
            data.append({
                "asset": r[0],
                "threat": r[1],
                "vulnerability": r[2],
                "likelihood": r[3],
                "impact": r[4],
                "risk_score": r[5],
                "risk_level": r[6]
            })
        return jsonify(data)
    except Exception as e:
        print(f"❌ DB error (TVA Mapping): {e}")
        return jsonify({"error": "Failed to fetch TVA data"}), 500
    finally:
        cursor.close()
        conn.close()

# ✅ 3. Threat Logs API
@app.route("/api/threats")
def get_threat_logs():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(""" 
            SELECT threat_type, risk_score, confidence, last_observed, source, details, ip_address 
            FROM tva_mapping.threat_intel_temp 
            ORDER BY last_observed DESC 
        """)
        rows = cursor.fetchall()
        data = []
        for r in rows:
            data.append({
                "type": r[0],
                "risk_score": r[1],
                "confidence": r[2],
                "timestamp": r[3].isoformat() if r[3] else "N/A",
                "source": r[4],
                "details": r[5],
                "ip": r[6] or "N/A"
            })
        return jsonify(data)
    except Exception as e:
        print(f"❌ DB error (threat logs): {e}")
        return jsonify({"error": "Failed to fetch threat logs"}), 500
    finally:
        cursor.close()
        conn.close()

# ✅ 4. Incident Response Playbook API
@app.route("/api/incidents", methods=["GET"])
def get_incident_responses():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute(""" 
            SELECT threat_type, risk_score, ip_address 
            FROM tva_mapping.threat_intel_temp 
            WHERE risk_score IS NOT NULL 
            ORDER BY last_observed DESC 
            LIMIT 10 
        """)
        rows = cursor.fetchall()
        responses = []

        for row in rows:
            threat_type = row[0].strip().lower()
            risk_score = row[1]
            ip = row[2] or "N/A"

            response = build_incident_response(threat_type, risk_score)
            response["threat_name"] = threat_type
            response["risk_score"] = risk_score
            response["ip"] = ip

            responses.append(response)

        return jsonify(responses)

    except Exception as e:
        print(f"❌ Error generating incident responses: {e}")
        return jsonify({"error": "Unable to fetch incident responses"}), 500
    finally:
        cursor.close()
        conn.close()

# ✅ Launch Server
if __name__ == "__main__":
    print("🚀 Flask server running at http://localhost:8080")
    app.run(host="0.0.0.0", port=8080, debug=True)
