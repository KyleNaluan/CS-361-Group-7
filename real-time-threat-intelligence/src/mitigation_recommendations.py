# mitigation_recommendations.py

def recommend_mitigation(threat_name):
    threat_name = threat_name.strip().lower()

    # Map aliases to canonical threat types
    aliases = {
        "sql injection": "sql injection",
        "sqli": "sql injection",

        "phishing": "phishing",
        "email scam": "phishing",

        "ddos": "ddos",
        "denial of service": "ddos",

        "ransomware": "ransomware",
        "crypto malware": "ransomware",

        "xss": "xss",
        "cross site scripting": "xss",

        "brute force": "brute force",
        "bruteforce": "brute force",
        "brute-force": "brute force",

        "unauthorized access": "unauthorized access",
        "privilege escalation": "unauthorized access"
    }

    # Central recommendation list
    recommendations = {
        "sql injection": "Use parameterized queries, sanitize inputs, enable a Web Application Firewall (WAF), and block malicious IP addresses.",
        "phishing": "Enable two-factor authentication, conduct employee training, deploy email filtering tools, and block malicious IP addresses.",
        "ddos": "Implement rate limiting, use load balancers, subscribe to DDoS protection services like Cloudflare, and block malicious IP addresses.",
        "ransomware": "Regularly backup data, restrict administrative privileges, use endpoint protection tools, and block malicious IP addresses.",
        "xss": "Use output encoding, content security policies (CSP), input validation, and block malicious IP addresses.",
        "brute force": "Implement account lockout mechanisms, enforce strong password policies, and block malicious IP addresses.",
        "unauthorized access": "Use role-based access controls (RBAC), audit user activity logs regularly, and block malicious IP addresses."
    }

    # Resolve threat name to canonical form
    canonical_name = aliases.get(threat_name, None)
    if canonical_name and canonical_name in recommendations:
        return recommendations[canonical_name]
    else:
        return "No recommendation available for this threat."


# Optional test block
if __name__ == "__main__":
    test_threats = ["SQLi", "Cross Site Scripting", "Brute-Force", "email scam", "weird threat"]
    for t in test_threats:
        print(f"{t}: {recommend_mitigation(t)}")
