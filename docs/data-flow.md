# Data Flow

1. Client uploads audio to `POST /v1/ingest/audio`.
2. API reads bytes into memory (`UploadFile.read`) and sends bytes to transcription service.
3. Transcript is optionally de-identified (Presidio + regex policy).
4. Raw audio buffer is purged in-memory before response.
5. Client sends transcript text to `POST /v1/note/generate`.
6. API calls local Ollama endpoint and validates structured note schema.
7. Client submits note + encounter + patient to `POST /v1/fhir/export`.
8. API returns FHIR Bundle JSON.

PHI exists in steps 1-3 and is reduced at step 3. Audit logs store only metadata/counts.
