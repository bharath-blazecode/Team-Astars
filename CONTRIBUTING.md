# Working on SpeedQ

The hackathon submission is complete. Improvements should preserve its synthetic-data demonstration and clearly distinguish new portfolio work from the historical submission.

1. Follow [BUILD.md](BUILD.md); use a separate `NRY_DB` for experiments.
2. Keep scoring, evidence ownership, draft confirmation and officer decision boundaries explicit.
3. Run `python tools/check_backend.py` for backend changes and `npm test` from `frontend/` for interface changes. Run `python tools/check_docs.py` after changing documentation or assets.
4. Never commit `.env`, API keys, SQLite databases, real customer records or private agent exports.
5. For visual updates, capture the running prototype rather than creating mock screenshots; use the original headset.
6. Describe observable behaviour and verification in the PR. Avoid unsupported impact, affiliation or live-integration claims.

Do not delete `web/` as a legacy folder: it serves the current customer and demo pages. The alternate `web/officer.html` and Streamlit `console/` are historical interfaces, retained without moving active imports.

Team-authored code has no repository-wide licence yet. A contribution or public visibility does not establish a general reuse grant; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
