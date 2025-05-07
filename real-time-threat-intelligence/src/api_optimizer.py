# api_optimizer.py

import time

# In-memory cache (only lives while app is running)
cache = {}

def fetch_from_osint(ip):
    print(f"Fetching data for {ip} from OSINT API...")
    time.sleep(1)  # Simulate API call delay
    return {"ip": ip, "threat": "Malicious IP", "risk_score": 42}

def get_threat_data(ip):
    if ip in cache:
        print(f"✅ Cache hit for {ip}")
        return cache[ip]
    else:
        print(f"❌ Cache miss for {ip}")
        result = fetch_from_osint(ip)
        cache[ip] = result
        return result

# Example usage
if __name__ == "__main__":
    print(get_threat_data("192.168.1.1"))
    print(get_threat_data("192.168.1.1"))  # Should hit cache
    print(get_threat_data("10.0.0.2"))     # New fetch
