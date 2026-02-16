# Test Plan (LLM)

## Testing Goals
Prove key invariants:
- Buffer-and-Purge (no audio stored)
- De-identification works for fixtures
- FHIR bundle valid structure
- Audit logs exclude PHI

## Required Tests

### 1) test_buffer_purge.py
- Simulate ingest with a small audio fixture (or mock transcription function).
- Assert:
  - audio bytes are processed in memory
  - no file is created in temp dirs
  - function explicitly deletes/clears buffers after use
- If implementation uses a BytesIO buffer, assert its size becomes 0 or object dereferenced.

### 2) test_deid.py
Provide text fixtures containing:
- Person name, phone, address, date, email, MRN-like pattern
Assert:
- Output replaces them with placeholders
- Entities list includes expected types
- No raw tokens remain

### 3) test_fhir_bundle.py
- Provide a sample note JSON and encounter metadata
- Generate bundle
Assert:
- top-level resourceType == "Bundle"
- contains Encounter
- contains Condition for each problem
- contains Observations for vitals if present
- resources include required fields minimally (status/category/code as needed)

### 4) test_audit_logs.py
- Use a log capture fixture
- Make a request with PHI text
- Assert logs do NOT contain the PHI text
- Assert logs DO contain correlation_id and event_name

## CI
In `.github/workflows/ci.yml`:
- install deps
- run pytest
- optionally run ruff/black checks
