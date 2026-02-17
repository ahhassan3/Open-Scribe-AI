# Open-Scribe-AI Whitepaper (MVP)

Open-Scribe-AI targets clinician documentation burden with a local-first architecture to reduce privacy risk and support on-prem deployment. The MVP includes secure audio ingestion, de-identification, note structuring, and FHIR export.

Security design: buffer-and-purge audio, PHI-safe logs, and local-only LLM routing to Ollama by default.

Limitations: this is not a diagnostic tool; clinician review is mandatory.

Evaluation approach: transcription latency, de-id precision/recall on fixtures, note schema validity rate, and end-to-end throughput.
