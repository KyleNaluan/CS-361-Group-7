-- Create a table to store threat intelligence data from Shodan
-- Each row represents the scan results for one IP address

CREATE TABLE public.threat_data (
    id SERIAL PRIMARY KEY,                           -- Unique identifier
    ip_address TEXT NOT NULL,                        -- IP address scanned
    ports JSONB,                                     -- Open ports
    services JSONB,                                  -- Hostnames or detected services
    fetched_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP -- Timestamp
);
