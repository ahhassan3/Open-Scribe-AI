# Open-Scribe-AI MVP

Local-first clinical scribe API with in-memory audio processing, PHI de-identification, local Ollama note generation, and FHIR export.

## Features
- Buffer-and-purge audio ingest (`/v1/ingest/audio`) without raw audio persistence.
- Presidio + custom regex de-identification.
- Local-only LLM orchestration through Ollama.
- Structured note generation validated by Pydantic schema.
- FHIR Bundle export (Encounter, Condition, Observation, DocumentReference).
- Correlation IDs + PHI-safe JSON audit logging.

## Quickstart (Docker Compose)
1. Copy environment file:
   ```bash
   cp .env.example .env
   ```
2. Start stack:
   ```bash
   docker compose -f infra/docker/docker-compose.yml up --build
   ```
3. Pull Ollama model (first run):
   ```bash
   docker compose -f infra/docker/docker-compose.yml exec ollama ollama pull llama3.1:8b
   ```

## API Examples

### Health
```bash
curl -s http://localhost:8000/v1/health
```

### Ingest audio
```bash
curl -s -X POST http://localhost:8000/v1/ingest/audio \
  -F "file=@examples/sample_inputs/sample.wav" \
  -F "deidentify=true"
```

### De-identify text
```bash
curl -s -X POST http://localhost:8000/v1/ingest/deidentify \
  -H 'Content-Type: application/json' \
  -d '{"text":"John Doe MRN 123456 email john@example.com"}'
```

### Generate note
```bash
curl -s -X POST http://localhost:8000/v1/note/generate \
  -H 'Content-Type: application/json' \
  -d '{"transcript_text":"Patient has cough for three days without fever"}'
```

### Export FHIR
```bash
curl -s -X POST http://localhost:8000/v1/fhir/export \
  -H 'Content-Type: application/json' \
  -d '{
    "note": {
      "chief_complaint":"cough",
      "hpi":"3 days",
      "ros":"no fever",
      "assessment_plan":"supportive care",
      "problems":[{"text":"cough","icd10":null,"snomed":null,"confidence":0.8}]
    },
    "encounter":{"start":"2026-02-13T10:00:00","end":"2026-02-13T10:20:00","class":"AMB","reason":"cough"},
    "patient":{"id":"example-patient-1"}
  }'
```

## Local Dev
```bash
pip install .[dev]
uvicorn apps.api.main:app --reload
pytest
```

## Human-required setup
See `HUMAN_ACTIONS.md`.
