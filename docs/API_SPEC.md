# API Specification (LLM)

## Global Rules
- All endpoints are versioned under `/v1`
- Every request should support a `X-Correlation-Id` header (optional). If missing, generate one.
- Return structured errors:
  {
    "error": { "code": "...", "message": "...", "details": {...}, "correlation_id": "..." }
  }

## Endpoints

### 1) Health
GET /v1/health
Response: { "status": "ok", "service": "open-scribe-api", "version": "0.1.0" }

### 2) Audio Ingest + Transcribe (Buffer-and-Purge)
POST /v1/ingest/audio
Content-Type: multipart/form-data
Form fields:
- file: audio file (wav/mp3/m4a/ogg)
- deidentify: bool (default true)
- language: optional string (e.g., "en")
- diarize: bool (default false, optional future)

Response 200:
{
  "transcript_id": "uuid",
  "correlation_id": "uuid",
  "transcript_text": "...",          // de-identified if requested
  "metadata": { "duration_sec": 123, "model": "whisper-local", "stored_audio": false }
}

Hard requirement: No raw audio written to disk.

### 3) Note Generation from Transcript
POST /v1/note/generate
Body:
{
  "transcript_id": "uuid (optional)",
  "transcript_text": "string",
  "patient_context": { "age": 40, "sex": "M" } (optional),
  "output_format": "json" (only json in MVP)
}

Response 200:
{
  "correlation_id": "uuid",
  "note": {
    "chief_complaint": "...",
    "hpi": "...",
    "ros": { "constitutional": "...", "cardiovascular": "...", ... },
    "assessment_plan": "...",
    "problems": [
      { "text": "hypertension", "icd10": null, "snomed": null, "confidence": 0.62 }
    ]
  },
  "model_info": { "llm": "ollama:<model>", "temperature": 0.2 }
}

MVP: allow ICD/SNOMED fields to be null; implement mapping later.

### 4) FHIR Export
POST /v1/fhir/export
Body:
{
  "note": { ...same as above... },
  "encounter": {
    "start": "2026-02-13T10:00:00",
    "end": "2026-02-13T10:20:00",
    "class": "AMB",
    "reason": "..."
  },
  "patient": {
    "id": "example-patient-1"   // placeholder in MVP
  }
}

Response 200:
{
  "correlation_id": "uuid",
  "fhir_bundle": { ...FHIR Bundle JSON... }
}

### 5) (Optional in MVP) De-identify text only
POST /v1/ingest/deidentify
Body: { "text": "..." }
Response: { "correlation_id": "uuid", "deidentified_text": "...", "entities": [...] }

## Authentication (MVP)
- For MVP, allow no auth locally.
- But implement a placeholder middleware for future:
  - API key header: `X-API-Key`
  - If configured in env, require it.
