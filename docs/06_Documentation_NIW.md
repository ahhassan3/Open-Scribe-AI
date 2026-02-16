# Documentation Artifacts (NIW + Engineering) — LLM Instructions

## Required docs to create
1. docs/whitepaper.md
2. docs/hhs-alignment.md
3. docs/threat-model.md
4. docs/data-flow.md
5. docs/benchmarks.md
6. docs/niw-evidence.md

## Content Requirements

### whitepaper.md
- Problem statement: admin burden, documentation, burnout
- System overview: on-prem, privacy-by-design
- Architecture: modules + flows
- Security: buffer-and-purge, de-id, audit logs
- Limitations: not a diagnostic tool; clinician review required
- Evaluation methodology: accuracy measures for section extraction + de-id coverage + latency

### hhs-alignment.md
- Quote minimal relevant excerpts from HHS AI Strategy (with citation links in prose)
- Map each pillar to a feature in this repo

### threat-model.md
- Identify risks and mitigations with concrete controls
- Include table: threat -> control -> test/evidence artifact

### data-flow.md
- Step-by-step data flow diagrams described in text
- Clearly state where PHI exists and where it is removed

### benchmarks.md
- Define what you measure:
  - transcription latency, note structuring accuracy (human-labeled sample), de-id precision/recall
- Avoid claiming clinical equivalence or decision-making

### niw-evidence.md
Create a table:
- Artifact -> Dhanasar prong(s) supported -> how to verify
Example:
- docker-compose on-prem demo -> well-positioned -> run compose and curl /health
- de-id tests -> substantial merit -> run pytest test_deid.py

## Citation Rule
When docs mention statistics or strategies, include citations as URLs or footnotes.
