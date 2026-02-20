# Database Architecture Decision

## Decision
Use a **relational database (PostgreSQL)** as the system-of-record for production artifacts.

## Why relational (vs non-relational)
A relational model is the better fit for this phase because the workflow is strongly structured and auditable:
- A transcript can produce multiple notes over time (versioning / retries).
- A note can produce multiple FHIR bundles.
- Correlation IDs and event lineage need deterministic joins for audits.
- Retention policies and compliance controls are easier to enforce with explicit relational constraints.

## Data that should be persisted
Persist only what is operationally needed and de-identified:
1. De-identified transcript text + redaction counts.
2. Structured note JSON + model metadata.
3. FHIR bundle JSON + encounter metadata.
4. PHI-safe audit metadata.

## Data that must NOT be persisted
- Raw audio bytes.
- Raw PHI-bearing transcript content if de-identification is disabled.
- Secrets, credentials, API keys.

## Schema assets
SQL scripts are under `/sql`:
- `001_init_schema.sql`
- `002_indexes.sql`
- `003_retention_cleanup.sql`
- `004_readiness_checks.sql`

## Recommended rollout path
1. Provision PostgreSQL (human action).
2. Apply SQL scripts in order.
3. Add application persistence adapter (repository pattern) writing only de-identified artifacts.
4. Add migration tracking (Flyway/Alembic) once schema stabilizes.
