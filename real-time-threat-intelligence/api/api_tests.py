import pytest
import sys
import os

# 🔧 Add api folder to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))

# ✅ Correct case-sensitive import
from ALLOSINT import virustotal_get_ip_report
from shodan_integration import fetch_shodan_data
from main import app

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'api', 'OSINT.env'))

def test_shodan_integration():
    ip = "8.8.8.8"
    data = fetch_shodan_data(ip)
    assert data is not None
    assert "ports" in data or "error" in data

def test_virustotal_integration():
    ip = "8.8.8.8"
    api_key = os.getenv("VIRUSTOTAL_API_KEY")
    assert api_key is not None
    data = virustotal_get_ip_report(ip, api_key)
    assert "reputation" in data

def test_flask_assets_api():
    with app.test_client() as client:
        response = client.get("/api/assets")
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)
