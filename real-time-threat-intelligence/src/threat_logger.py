import logging
import os

# Ensure log folder exists
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(filename='logs/threat_events.log', level=logging.INFO)

def log_threat(threat, risk_score):
    log_entry = f"{threat} detected with risk score: {risk_score}"
    logging.info(log_entry)
    print(f"✅ Logged: {log_entry}")  # <- THIS LINE

# Example usage
if __name__ == "__main__":
    log_threat("DDoS Attack", 30)
