# HUMAN ACTIONS REQUIRED

The following tasks require a human operator and cannot be completed autonomously by the code agent.

## 1) Install host prerequisites
1. Install Docker Engine / Docker Desktop.
2. Verify compose plugin: `docker compose version`.
3. (Optional GPU) Install NVIDIA driver + CUDA toolkit + nvidia-container-toolkit.

## 2) Pull local models
1. Start stack: `docker compose -f infra/docker/docker-compose.yml up -d ollama`.
2. Pull the model set in `.env`:
   `docker compose -f infra/docker/docker-compose.yml exec ollama ollama pull llama3.1:8b`.
3. If using local transcription model variants, ensure whisper model files can be downloaded by `faster-whisper` runtime.

## 3) Secrets and key policy
1. Decide whether to enable API key protection (`REQUIRE_API_KEY=true`).
2. Generate and store API key in secure secret management tool.
3. Inject the key into runtime `.env` or orchestrator secret store.

## 4) TLS for non-local deployments
1. Obtain TLS certificate (internal PKI or public CA).
2. Configure reverse proxy (Nginx/Caddy/Ingress) in front of FastAPI.
3. Enforce HTTPS-only traffic and certificate rotation policy.

## 5) Infrastructure provisioning
1. Provision on-prem host(s) with enough CPU/RAM/GPU for Ollama and Whisper.
2. Configure firewall rules for ports 8000 and 11434 (or internal-only).
3. Set monitoring/alerting and log retention policy per organization standards.

## 6) Compliance and governance decisions
1. Run HIPAA/privacy/compliance review.
2. Approve data retention policy and acceptable-use policy.
3. Validate clinical workflow with clinician oversight before production use.

## 7) Operational validation
1. Execute end-to-end curl flow from README.
2. Run `pytest` and archive test evidence for audits.
3. Perform penetration/security testing in your target environment.
