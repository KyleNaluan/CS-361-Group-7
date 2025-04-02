
def recommend_mitigation(threat_name):

    threat_name = threat_name.strip().lower()

    recommendations = {
        "sql injection": "Use parameterized queries, sanitize inputs, and enable a Web Application Firewall (WAF).",
        "phishing": "Enable two-factor authentication, conduct employee training, and deploy email filtering tools.",
        "ddos": "Implement rate limiting, use load balancers, and subscribe to DDoS protection services like Cloudflare.",
        "ransomware": "Regularly backup data, restrict administrative privileges, and use endpoint protection tools.",
        "xss": "Use output encoding, content security policies (CSP), and input validation.",
        "brute force": "Implement account lockout mechanisms and enforce strong password policies.",
        "unauthorized access": "Use role-based access controls (RBAC) and audit user activity logs regularly.",
    }

    return recommendations.get(threat_name, "No recommendation available for this threat.")
