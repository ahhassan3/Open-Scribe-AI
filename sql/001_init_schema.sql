-- Open-Scribe-AI canonical relational schema (PostgreSQL 15+)
-- Principle: store de-identified artifacts + metadata only.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS scribe;

CREATE TABLE IF NOT EXISTS scribe.transcript (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transcript_hash CHAR(64) NOT NULL UNIQUE,
    transcript_text_deid TEXT NOT NULL,
    deidentify_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    entities_redacted INTEGER NOT NULL DEFAULT 0,
    source_content_type TEXT,
    model_name TEXT,
    correlation_id UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (entities_redacted >= 0)
);

CREATE TABLE IF NOT EXISTS scribe.note (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transcript_id UUID NOT NULL REFERENCES scribe.transcript(id) ON DELETE CASCADE,
    note_json JSONB NOT NULL,
    problem_count INTEGER NOT NULL DEFAULT 0,
    llm_model TEXT NOT NULL,
    llm_temperature NUMERIC(4,3) NOT NULL DEFAULT 0.200,
    schema_version TEXT NOT NULL DEFAULT 'v1',
    correlation_id UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (problem_count >= 0)
);

CREATE TABLE IF NOT EXISTS scribe.fhir_bundle (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    note_id UUID NOT NULL REFERENCES scribe.note(id) ON DELETE CASCADE,
    bundle_json JSONB NOT NULL,
    patient_ref TEXT,
    encounter_class TEXT,
    encounter_start TIMESTAMPTZ,
    encounter_end TIMESTAMPTZ,
    correlation_id UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS scribe.audit_event (
    id BIGSERIAL PRIMARY KEY,
    event_name TEXT NOT NULL,
    action TEXT,
    status TEXT,
    correlation_id UUID,
    details JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE scribe.transcript IS 'Stores de-identified transcript artifacts only; never raw audio.';
COMMENT ON TABLE scribe.note IS 'Stores structured note generated from transcript.';
COMMENT ON TABLE scribe.fhir_bundle IS 'Stores FHIR bundle exports for replay/audit.';
COMMENT ON TABLE scribe.audit_event IS 'Metadata-only audit log (PHI-safe).';
