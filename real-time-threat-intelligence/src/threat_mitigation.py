# Function for automated response system
def automated_response(threat):
    responses = {
        "SQL Injection": "Apply Web Application Firewall (WAF) rules.",
        "Phishing": "Enforce 2FA for all users.",
        "DDoS Attack": "Activate rate limiting and blackhole routing."
    }
    return responses.get(threat, "No automatic response available.")

# Example Usage
threat = "Phishing"
action = automated_response(threat)
print(f"Recommended Action: {action}")
