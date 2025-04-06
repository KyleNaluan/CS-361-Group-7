CREATE TABLE schema.incident_logs (
    id SERIAL PRIMARY KEY,
    threat_name VARCHAR(255),
    risk_score INT,
    priority VARCHAR(50),
    nist_phases TEXT,
    response_steps TEXT,
    timestamp TIMESTAMP
);