-- Week 5 - Task 2: Refine TVA Mapping based on threat intelligence

UPDATE tva_mapping.tva_mapping
SET likelihood = 5,
    impact = 5
WHERE threat_name IN (
    'Phishing Risk',
    'Broken Authentication'
);
