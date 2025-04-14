# Security Audit

**Project:** OSINT Threat Intelligence System  
**Date:** April 2025  
**Conducted By:** Group 7  

# As our project is right now, the tools are unable to retrive information so everything is TBD #
# After future updates, this file will also be updated with new information #

## Tools 

| Tools  used | Version | Purpose                                 |

| Nmap        | TBD     | Scan for open ports and services        |
| OWASP ZAP   | TBD     | Scan for web app vulnerabilities        |
| Burp Suite  | TBD     | Analyze HTTP requests/responses         |

---

## Target

| Component           | Description                      |

| Localhost app/API   | Threat fetcher and risk scoring  |
| IP scanned          | 127.0.0.1 (loopback interface)   |

---

## Findings

| Tool       | Finding                          | Severity | Recommendation               |

| Nmap       | TBD                              | TBD      | TBD                           |
| ZAP        | TBD                              | TBD      | TBD                           |
| Burp Suite | TBD                              | TBD      | TBD                           |

---

## Remediation Steps ##

-Close unnecessary ports
-Add security headers
-Secure cookies with flags (`Secure`, `HttpOnly`)
-Validate & sanitize all user input

---


## How to generate info for report ##

1. Run Nmap scan with:
nmap -A -T4 -oN nmap_scan_results.txt localhost
(this should open ports and sevice on loacal host)

2. Scan with OWASP ZAP
Open up ZAP
Enter the app URL http://localhost:5000
Run spider and active scan tools
Export results if needed

3.Burp suite:

Set the browser proxy to 127.0.0.1:8080
Move throught he app manually
Watch HTTP traffic and look for things like
-Insecure cookies
-Misconfigurations
-Vulnerable parameters