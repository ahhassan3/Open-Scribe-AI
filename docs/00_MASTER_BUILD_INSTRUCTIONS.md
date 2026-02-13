# Open-Scribe-AI — Master Build Instructions (LLM-Executable)

## Objective
Build a working, local-first (on-prem) clinical scribe framework that:
- Ingests audio (no raw audio persistence)
- Transcribes with local Whisper
- De-identifies PHI/PII using Presidio + policy rules
- Extracts structured note fields (Chief Complaint, HPI, ROS, Assessment & Plan)
- Maps to FHIR Bundle (Encounter, Condition, Observation, DocumentReference optional)
- Runs fully on-prem via Docker Compose (FastAPI + Ollama + optional local stores)
- Includes unit/integration tests proving privacy invariants (buffer-and-purge, de-id)

## Non-Negotiable Constraints
1. **Buffer-and-Purge**: Raw audio must not be stored on disk. It may only exist in memory during processing.
2. **Local inference by default**: Use Ollama for LLM; no cloud LLM calls.
3. **PHI protection**: Provide de-identification stage (Presidio) + policy stage (custom rules).
4. **Auditability**: Produce structured audit logs for key events (ingest, de-id, note generation, export).
5. **Reproducibility**: `docker-compose.yml` must run everything locally.

## Repository Deliverables
You MUST generate all of these:
- A complete repo structure (see `docs/01_REPO_SCAFFOLD.md`)
- Working FastAPI app with documented endpoints (see `docs/02_API_SPEC.md`)
- Services: audio processing, de-id, NLP extraction, fhir mapping
- Middleware for security guard + audit logs (see `docs/03_SECURITY_PRIVACY.md`)
- On-prem Docker Compose (see `docs/04_LOCAL_DEPLOYMENT.md`)
- Tests (see `docs/05_TEST_PLAN.md`)
- Documentation artifacts (see `docs/06_DOCUMENTATION_NIW.md`)
- A backlog/roadmap (see `docs/07_BACKLOG_ROADMAP.md`)

## REQUIRED: Human Actions List (things you cannot do)
You MUST create a file at repo root named `HUMAN_ACTIONS.md` listing:
- Any step requiring human action, external accounts, credentials, infrastructure provisioning, legal review, or decisions.
- Any step you can’t perform because it requires running commands in a real environment or accessing private networks.
Include step-by-step instructions for the human to complete those items.

Examples to include:
- Setting up a database server or managed storage (if used)
- Obtaining/rotating encryption keys, setting KMS/HSM
- Issuing real TLS certificates and configuring DNS
- HIPAA compliance review and organizational policies
- Installing Docker/WSL2 and GPU drivers
- Downloading specific Ollama/Whisper models (if not auto-downloaded)

## Implementation Guidelines
- Language: Python 3.11+
- API: FastAPI + Uvicorn
- LLM orchestration: LangChain + Ollama
- Transcription: local Whisper (prefer `faster-whisper` if possible)
- De-identification: Microsoft Presidio (Analyzer + Anonymizer)
- FHIR: `fhir.resources` (R4), output JSON bundle
- Testing: pytest
- Linting/formatting: ruff + black (optional but recommended)

## Acceptance Criteria
The following must work end-to-end:
1. `POST /v1/ingest/audio` -> returns `transcript_id` and transcript text (de-identified option configurable)
2. `POST /v1/note/generate` with transcript -> returns structured JSON note sections
3. `POST /v1/fhir/export` with structured note -> returns valid FHIR Bundle JSON
4. `docker compose up` -> boots services locally
5. Tests pass: buffer-and-purge, de-id fixture tests, fhir bundle validation, audit log generation

## What to do first
1. Create repo skeleton (01)
2. Implement config + logging primitives
3. Implement ingestion -> transcription -> purge
4. Implement de-id pipeline
5. Implement note generation pipeline
6. Implement fhir mapper
7. Add docker-compose + docs + tests
