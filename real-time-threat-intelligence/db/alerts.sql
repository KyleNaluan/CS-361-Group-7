-- Drop the old alert_logs table if it exists
DROP TABLE IF EXISTS public.alert_logs;

-- Create the new simplified alert_logs table
CREATE TABLE public.alert_logs (
    id SERIAL PRIMARY KEY,
    threat_name VARCHAR(255) NOT NULL,
    risk_score INT NOT NULL,
    alert_type VARCHAR(50) DEFAULT 'Email',  -- Default alert type as Email
    is_sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
