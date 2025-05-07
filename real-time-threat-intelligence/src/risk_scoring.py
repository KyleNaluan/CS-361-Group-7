import datetime

def calculate_risk(likelihood, impact, last_seen):
    days_since_last_seen = (datetime.datetime.now() - last_seen).days
    decay_factor = max(0.1, 1 - (0.05 * days_since_last_seen))
    return round((likelihood * impact) * decay_factor, 2)

# Example
if __name__ == "__main__":
    risk_score = calculate_risk(4, 5, datetime.datetime(2025, 3, 20))
    print(f"Updated Risk Score: {risk_score}")
