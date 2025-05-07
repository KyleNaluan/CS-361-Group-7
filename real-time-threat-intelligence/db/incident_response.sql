CREATE OR REPLACE VIEW tva_mapping.incident_response AS
SELECT
    threat_type,
    risk_score,
    confidence,
    ip_address,
    last_observed,
    source,
    details
FROM tva_mapping.threat_intel_temp
WHERE risk_score IS NOT NULL
ORDER BY last_observed DESC;
