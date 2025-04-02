# risk_prioritization.py

def calculate_risk_score(vt_score, abuse_score, total_reports):
    """
    Weighted scoring model:
    - VirusTotal reputation (0-100): weight 0.4
    - AbuseIPDB confidence (0-100): weight 0.4
    - Number of reports (max 100): weight 0.2
    """
    total_reports = min(total_reports, 100)  # cap at 100
    score = (vt_score * 0.4) + (abuse_score * 0.4) + (total_reports * 0.2)
    return round(score, 2)



def prioritize_risks(threats):
    """
    Sort threats by descending risk score.
    """
    return sorted(threats, key=lambda x: x["risk_score"], reverse=True)


# Example usage (optional test)
if __name__ == "__main__":
    threats = [
        {"name": "SQL Injection", "risk_score": 20},
        {"name": "Phishing", "risk_score": 30},
        {"name": "DDoS", "risk_score": 25}
    ]
    prioritized = prioritize_risks(threats)
    print("🔝 Top threats by risk score:")
    for threat in prioritized:
        print(f"{threat['name']}: {threat['risk_score']}")

