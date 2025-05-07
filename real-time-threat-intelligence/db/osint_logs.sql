-- Creates a table to store historical OSINT data
CREATE TABLE public.osint_logs (
    id SERIAL PRIMARY KEY,
    ip TEXT NOT NULL,
    vt_reputation INTEGER,
    abuse_score INTEGER,
    total_reports INTEGER,
    domain TEXT,
    created_date TEXT,
    registrar TEXT,
    fetched_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
