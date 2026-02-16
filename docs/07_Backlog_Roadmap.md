# Backlog & Roadmap (LLM)

## MVP (must ship first)
- Audio ingest + local transcription
- Buffer-and-purge guarantee + test
- De-id pipeline + test fixtures
- Note generation via Ollama with structured JSON schema
- FHIR export Bundle
- Docker compose on-prem
- Basic audit logs

## Next (v0.2)
- Speaker diarization (optional)
- ICD-10 + SNOMED mapping plugin interface
- Patient/Encounter ID handling improvements
- Local persistence with encryption at rest (optional)
- RBAC + API key auth enabled by default
- UI prototype (simple web page)

## v0.3+
- FHIR validation improvements + profiles
- Multi-language support
- Offline terminology dictionary integration
- Clinic deployment guide + hardening checklists
- Performance tuning + batching

## Non-Goals / Guardrails
- Not a diagnostic system
- Must require clinician review
- No cloud LLM calls in default mode
