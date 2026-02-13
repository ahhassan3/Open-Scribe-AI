# Repo Scaffold Instructions (LLM)

## Create the following directory structure
open-scribe-ai/
  apps/
    api/
      main.py
      api/
        __init__.py
        routes/
          __init__.py
          health.py
          ingest.py
          note.py
          fhir.py
      core/
        __init__.py
        config.py
        logging.py
        security.py
      middleware/
        __init__.py
        hipaa_guard.py
      services/
        __init__.py
        audio_proc.py
        whisper_local.py
        deid.py
        nlp_engine.py
        llm_orchestrator.py
        fhir_mapper.py
      models/
        __init__.py
        schemas.py
      tests/
        __init__.py
        test_buffer_purge.py
        test_deid.py
        test_fhir_bundle.py
        test_audit_logs.py

  infra/
    docker/
      Dockerfile.api
      docker-compose.yml
      ollama/
        README.md

  docs/
    00_MASTER_BUILD_INSTRUCTIONS.md
    01_REPO_SCAFFOLD.md
    02_API_SPEC.md
    03_SECURITY_PRIVACY.md
    04_LOCAL_DEPLOYMENT.md
    05_TEST_PLAN.md
    06_DOCUMENTATION_NIW.md
    07_BACKLOG_ROADMAP.md

  examples/
    sample_inputs/
    sample_outputs/
    fhir_bundles/

  .github/
    workflows/
      ci.yml

  .env.example
  pyproject.toml
  README.md
  LICENSE
  HUMAN_ACTIONS.md   <-- REQUIRED OUTPUT FILE

## Files to generate with basic content
1. README.md: high-level overview + quickstart for docker compose + local dev steps.
2. LICENSE: Apache-2.0 text or reference.
3. .env.example: list config keys (no secrets).
4. pyproject.toml: deps + tooling config.
5. Each package __init__.py as needed.

## Configuration philosophy
- Use environment variables (12-factor).
- Provide a Settings object in `core/config.py` using pydantic-settings.
- No secrets committed. Use `.env` locally (gitignored).

## Logging philosophy
- JSON logs, consistent fields:
  - event_name, timestamp, correlation_id, user_id (if any), request_id, action, status, details
- Store logs to stdout; docker can capture them.

## Dependency list (minimum)
- fastapi
- uvicorn[standard]
- pydantic
- pydantic-settings
- python-multipart (file upload)
- langchain (or langchain-community as needed)
- ollama python client OR simple HTTP call to Ollama
- presidio-analyzer
- presidio-anonymizer
- fhir.resources
- pytest

Optionals:
- faster-whisper
- cryptography
- ruff, black

## REQUIRED: HUMAN_ACTIONS.md
Ensure root contains HUMAN_ACTIONS.md with tasks the LLM cannot do.
