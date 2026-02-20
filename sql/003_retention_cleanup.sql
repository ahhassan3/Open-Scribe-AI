-- Retention housekeeping queries (run via cron / pg_cron / scheduler)
-- Example policy: keep artifacts 365 days, audit metadata 90 days.

DELETE FROM scribe.audit_event
WHERE created_at < NOW() - INTERVAL '90 days';

DELETE FROM scribe.fhir_bundle
WHERE created_at < NOW() - INTERVAL '365 days';

DELETE FROM scribe.note
WHERE created_at < NOW() - INTERVAL '365 days';

DELETE FROM scribe.transcript
WHERE created_at < NOW() - INTERVAL '365 days';
