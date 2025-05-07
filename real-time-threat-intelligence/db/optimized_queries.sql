-- Create index on threat_type field to optimize queries
CREATE INDEX idx_threat_type ON threat_data(threat_type);

-- Example of a query that will benefit from this index
EXPLAIN ANALYZE SELECT * FROM threat_data WHERE threat_type = 'SQL Injection';
