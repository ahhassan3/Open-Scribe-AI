# NIW Evidence Mapping

| Artifact | Dhanasar Prong(s) | Verification |
|---|---|---|
| Docker compose local stack | Well-positioned | `docker compose -f infra/docker/docker-compose.yml up --build` |
| De-identification tests | Substantial merit | `pytest apps/api/tests/test_deid.py` |
| Buffer-purge tests | National importance/privacy | `pytest apps/api/tests/test_buffer_purge.py` |
| FHIR export endpoint | Practical utility | `curl POST /v1/fhir/export` |
