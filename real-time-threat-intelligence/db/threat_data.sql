-- Create a table to store threat intelligence data from Shodan
-- Each row represents the scan results for one IP address

CREATE TABLE schema.threat_data (
    id SERIAL PRIMARY KEY,               -- Unique identifier for each record
    ip_address TEXT NOT NULL,            -- The scanned IP address
    ports JSONB,                         -- List of open ports (from Shodan)
    services JSONB,                      -- Hostnames or services (from Shodan)
    fetched_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP -- Time of data collection
);
