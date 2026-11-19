# SpeedQ backend

FastAPI serves the officer UI, customer/demo pages, intake tools and deterministic Prorio engine. The hackathon prototype was completed and submitted on **17 November 2026**.

From the repository root, follow [BUILD.md](../BUILD.md) for Windows or macOS/Linux setup. From `backend/` with dependencies installed:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Use one worker. No separate frontend process is required. The default loopback demo uses synthetic data; configured staff accounts enable prototype Basic authentication, not production SSO/MFA.

- [Architecture, persisted state and process-local limits](../docs/architecture.md)
- [API, scoring, protocol and environment reference](../docs/reference/TECHNICAL_REFERENCE.md)
- [External Retell configuration](../docs/live-services.md)
- [Validation commands](../BUILD.md#validation)
- [Protocol source notes](data/PROTOCOLS_SOURCES.md)

SQLite persists cases, drafts, ownership, audit records and approved protocol versions. `NRY_DB` selects another database; the default is ignored `backend/nry.db`. The reset operation clears the selected workspace, so use a separate database for rehearsals.

Prorio uses structured fields and owned evidence; free-text summaries do not determine rank. Its outputs are deterministic for the same inputs, evidence, time and active protocol. All banking effects remain simulated or draft records.

Live Retell integration code is included. The hosted agents, prompts, knowledge base and account configuration are external. Fake-client tests do not prove a live call or phone transfer succeeded in the submitted recording.
