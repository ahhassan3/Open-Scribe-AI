# Threat Model

| Threat | Control | Evidence |
|---|---|---|
| Raw audio persistence | In-memory byte buffer only, explicit purge path, no temp file usage | `apps/api/services/audio_proc.py`, `apps/api/tests/test_buffer_purge.py` |
| PHI in logs | PHI-safe metadata-only audit logs and correlation IDs | `apps/api/middleware/hipaa_guard.py`, `apps/api/tests/test_audit_logs.py` |
| Cloud LLM leakage | Ollama-only URL guardrail unless explicitly overridden | `apps/api/services/llm_orchestrator.py` |
| Weak access control | Optional API key middleware enforcement | `apps/api/middleware/hipaa_guard.py` |
| Re-identification in transcript | Presidio + custom regex redaction (MRN/email) | `apps/api/services/deid.py`, `apps/api/tests/test_deid.py` |
