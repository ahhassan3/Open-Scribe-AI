# Human Actions Required (Things the LLM Cannot Do)

This file lists steps requiring human action, external access, credentials, or real infrastructure.

## Environment setup
- Install Docker Desktop (and WSL2 on Windows) and verify `docker compose` works.
- (Optional) Install NVIDIA drivers + CUDA + container toolkit for GPU acceleration.

## Model acquisition
- Download/pull Ollama model(s): `ollama pull <model>`
- Obtain Whisper model files if required by chosen transcription library.

## Security / Compliance decisions
- Decide organizational HIPAA policies, retention rules, and audit requirements.
- If enabling TLS in non-local environments:
  - Obtain TLS certificates (or set up internal CA)
  - Configure DNS and reverse proxy endpoints

## Key management
- If enabling encryption at rest:
  - Generate and securely store master keys (prefer KMS/HSM)
  - Rotate keys and manage access

## Deployment
- Provision on-prem server(s) or clinic hardware
- Configure firewall rules, network access, and backups (if any storage is enabled)

## Validation
- Run real clinical test cases with clinician review and collect feedback.
