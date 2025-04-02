
CREATE TABLE IF NOT EXISTS tva_mapping.threat_intel_temp (
    id SERIAL PRIMARY KEY,
    threat_type VARCHAR(255),
    risk_score INT,
    confidence INT,
    last_observed TIMESTAMP,
    source VARCHAR(100),
    details TEXT
);

TRUNCATE tva_mapping.threat_intel_temp;

INSERT INTO tva_mapping.threat_intel_temp (threat_type, risk_score, confidence, last_observed, source, details)
VALUES
    ('SQL Injection', 22, 8, NOW() - INTERVAL '2 days', 'OWASP Top 10', 'Increased SQLi activity targeting financial institutions'),
    ('Phishing Attack', 25, 9, NOW() - INTERVAL '1 day', 'PhishTank', 'New sophisticated phishing campaign targeting corporate users'),
    ('DDoS Attack', 18, 7, NOW() - INTERVAL '5 days', 'DDoS-DB', 'Multiple botnets actively targeting cloud services'),
    ('Credential Stuffing', 23, 8, NOW() - INTERVAL '3 days', 'HaveIBeenPwned', 'New breach data being used in credential stuffing attacks'),
    ('Man-in-the-Middle Attack', 15, 6, NOW() - INTERVAL '7 days', 'ThreatFeed', 'Public WiFi MITM attacks increasing in urban areas');

UPDATE tva_mapping.tva_mapping
SET likelihood = CASE
    WHEN (SELECT risk_score FROM tva_mapping.threat_intel_temp WHERE threat_type = 'SQL Injection') > 20 THEN 5
    WHEN (SELECT risk_score FROM tva_mapping.threat_intel_temp WHERE threat_type = 'SQL Injection') > 15 THEN 4
    WHEN (SELECT risk_score FROM tva_mapping.threat_intel_temp WHERE threat_type = 'SQL Injection') > 10 THEN 3
    ELSE likelihood
END
WHERE threat_name = 'SQL Injection';

UPDATE tva_mapping.tva_mapping
SET likelihood = CASE
    WHEN (SELECT risk_score FROM tva_mapping.threat_intel_temp WHERE threat_type = 'Phishing Attack') > 20 THEN 5
    WHEN (SELECT risk_score FROM tva_mapping.threat_intel_temp WHERE threat_type = 'Phishing Attack') > 15 THEN 4
    ELSE likelihood
END
WHERE threat_name = 'Phishing Attack';


UPDATE tva_mapping.tva_mapping tm
SET impact = CASE
    WHEN a.asset_type = 'People' AND (SELECT risk_score FROM tva_mapping.threat_intel_temp WHERE threat_type = 'Phishing Attack') > 20 THEN 5
    ELSE impact
END
FROM assets.assets a
WHERE tm.asset_id = a.id
AND tm.threat_name = 'Phishing Attack';

UPDATE tva_mapping.tva_mapping
SET likelihood = CASE
    WHEN (SELECT risk_score FROM tva_mapping.threat_intel_temp WHERE threat_type = 'DDoS Attack') > 15 THEN 4
    WHEN (SELECT risk_score FROM tva_mapping.threat_intel_temp WHERE threat_type = 'DDoS Attack') > 10 THEN 3
    ELSE likelihood
END
WHERE threat_name = 'DDoS Attack';

UPDATE tva_mapping.tva_mapping tm
SET impact = CASE
    WHEN a.asset_type = 'Software' AND a.asset_name LIKE '%Web%' THEN 5
    ELSE impact
END
FROM assets.assets a
WHERE tm.asset_id = a.id
AND tm.threat_name = 'DDoS Attack';

UPDATE tva_mapping.tva_mapping
SET likelihood = CASE
    WHEN (SELECT risk_score FROM tva_mapping.threat_intel_temp WHERE threat_type = 'Credential Stuffing') > 20 THEN 5
    WHEN (SELECT risk_score FROM tva_mapping.threat_intel_temp WHERE threat_type = 'Credential Stuffing') > 15 THEN 4
    ELSE likelihood
END
WHERE threat_name = 'Credential Stuffing';

UPDATE tva_mapping.tva_mapping tm
SET impact = CASE
    WHEN a.asset_type = 'Data' AND a.asset_name LIKE '%Credentials%' THEN 5
    ELSE impact
END
FROM assets.assets a
WHERE tm.asset_id = a.id
AND tm.threat_name = 'Credential Stuffing';

UPDATE tva_mapping.tva_mapping
SET likelihood = CASE
    WHEN (SELECT risk_score FROM tva_mapping.threat_intel_temp WHERE threat_type = 'Man-in-the-Middle Attack') > 15 THEN 4
    WHEN (SELECT risk_score FROM tva_mapping.threat_intel_temp WHERE threat_type = 'Man-in-the-Middle Attack') > 10 THEN 3
    ELSE likelihood
END
WHERE threat_name = 'Man-in-the-Middle Attack';

CREATE TABLE IF NOT EXISTS tva_mapping.tva_update_log (
    id SERIAL PRIMARY KEY,
    update_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    update_source VARCHAR(255),
    threat_name VARCHAR(255),
    old_likelihood INTEGER,
    new_likelihood INTEGER,
    old_impact INTEGER,
    new_impact INTEGER,
    old_risk_score INTEGER,
    new_risk_score INTEGER
);

INSERT INTO tva_mapping.tva_update_log 
(update_source, threat_name, old_likelihood, new_likelihood, old_impact, new_impact, old_risk_score, new_risk_score)
SELECT 
    'Threat Intelligence Feed' as update_source,
    tm.threat_name,
    tva_before.likelihood as old_likelihood,
    tm.likelihood as new_likelihood,
    tva_before.impact as old_impact,
    tm.impact as new_impact,
    tva_before.risk_score as old_risk_score,
    tm.risk_score as new_risk_score
FROM 
    tva_mapping.tva_mapping tm
JOIN 
    (SELECT id, likelihood, impact, risk_score FROM tva_mapping.tva_mapping BEFORE UPDATE) as tva_before
ON 
    tm.id = tva_before.id
WHERE 
    tm.likelihood != tva_before.likelihood OR tm.impact != tva_before.impact;

CREATE OR REPLACE VIEW tva_mapping.tva_intel_view AS
SELECT 
    tm.id,
    a.asset_name,
    a.asset_type,
    tm.threat_name,
    tm.vulnerability_description,
    tm.likelihood,
    tm.impact,
    tm.risk_score,
    CASE
        WHEN tm.risk_score >= 16 THEN 'Critical'
        WHEN tm.risk_score >= 10 THEN 'High'
        WHEN tm.risk_score >= 4 THEN 'Medium'
        ELSE 'Low'
    END as risk_level,
    ti.risk_score as threat_intel_score,
    ti.confidence as threat_intel_confidence,
    ti.last_observed as threat_last_observed,
    ti.source as intel_source
FROM 
    tva_mapping.tva_mapping tm
JOIN 
    assets.assets a ON tm.asset_id = a.id
LEFT JOIN 
    tva_mapping.threat_intel_temp ti ON tm.threat_name = ti.threat_type
ORDER BY 
    tm.risk_score DESC;
