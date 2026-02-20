-- Operational checks for go-live

-- 1) Row counts by artifact class
SELECT 'transcript' AS table_name, COUNT(*) AS row_count FROM scribe.transcript
UNION ALL
SELECT 'note', COUNT(*) FROM scribe.note
UNION ALL
SELECT 'fhir_bundle', COUNT(*) FROM scribe.fhir_bundle
UNION ALL
SELECT 'audit_event', COUNT(*) FROM scribe.audit_event;

-- 2) Validate no obvious raw-audio content-type persisted
SELECT id, source_content_type, created_at
FROM scribe.transcript
WHERE source_content_type ILIKE '%audio/%'
ORDER BY created_at DESC
LIMIT 20;

-- 3) Spot-check notes with missing problems array (schema drift)
SELECT id, created_at
FROM scribe.note
WHERE NOT (note_json ? 'problems')
ORDER BY created_at DESC
LIMIT 20;
