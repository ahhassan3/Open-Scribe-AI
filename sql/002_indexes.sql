-- Performance + ops indexes

CREATE INDEX IF NOT EXISTS ix_transcript_created_at ON scribe.transcript(created_at DESC);
CREATE INDEX IF NOT EXISTS ix_transcript_corr_id ON scribe.transcript(correlation_id);

CREATE INDEX IF NOT EXISTS ix_note_transcript_id ON scribe.note(transcript_id);
CREATE INDEX IF NOT EXISTS ix_note_created_at ON scribe.note(created_at DESC);
CREATE INDEX IF NOT EXISTS ix_note_corr_id ON scribe.note(correlation_id);
CREATE INDEX IF NOT EXISTS ix_note_json_gin ON scribe.note USING GIN (note_json);

CREATE INDEX IF NOT EXISTS ix_bundle_note_id ON scribe.fhir_bundle(note_id);
CREATE INDEX IF NOT EXISTS ix_bundle_created_at ON scribe.fhir_bundle(created_at DESC);
CREATE INDEX IF NOT EXISTS ix_bundle_json_gin ON scribe.fhir_bundle USING GIN (bundle_json);

CREATE INDEX IF NOT EXISTS ix_audit_event_created_at ON scribe.audit_event(created_at DESC);
CREATE INDEX IF NOT EXISTS ix_audit_event_name ON scribe.audit_event(event_name);
CREATE INDEX IF NOT EXISTS ix_audit_event_corr_id ON scribe.audit_event(correlation_id);
CREATE INDEX IF NOT EXISTS ix_audit_event_details_gin ON scribe.audit_event USING GIN (details);
