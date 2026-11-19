# Build, run and verify SpeedQ

The hackathon submission is **complete (17 November 2026)**. This guide reproduces the prototype; it is not an outstanding submission checklist. See the [README](README.md) for the product and [submission record](docs/submission/README.md) for the final video/deck.

## Requirements

- Python **3.12+** with pip and venv.
- A modern browser. No frontend build or Node server is required.
- Node **22.12+** only for browser tests and screenshot generation.
- Internet for initial dependency installation. Retell credentials only for optional live services.

## Windows

Extract the **whole** repository ZIP, then double-click `START_WINDOWS.cmd`. It creates `.dashboard-venv`, installs requirements if needed and starts a loopback server. Keep the terminal open.

PowerShell alternative, from the repository root:

```powershell
py -3 run_dashboard.py --demo
```

Defaults: dashboard `http://127.0.0.1:8010/`, guided wrapper `http://127.0.0.1:8010/demo`. If the port is occupied by another service, run `py -3 run_dashboard.py --port 8011 --demo`. Do not assume an existing dashboard process is the latest checkout: stop your old instance before testing an update.

To run tests in the launcher's Python environment:

```powershell
.\.dashboard-venv\Scripts\python.exe tools/check_backend.py
```

The cleanup replaces the non-portable Unix `%-d` date directive used in card-delivery proposals. Windows CI is configured, but a native Windows pass is not claimed until that workflow runs successfully.

## macOS / Linux

From the repository root:

```bash
python3 -m venv backend/.venv
source backend/.venv/bin/activate
python -m pip install -r backend/requirements.txt
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Keep **one worker**. Open the printed local address. The launcher is also cross-platform: `python3 run_dashboard.py --demo` creates its own `.dashboard-venv`.

## Routes and data

| Route | Purpose |
|---|---|
| `/` or `/officer` | Current officer workspace |
| `/demo` | Full-width officer demonstration; optional customer preview from Live intake |
| `/customer` | Customer app, scripted scenes and configured live Clario |
| `/docs` | Self-hosted API reference, under staff access controls |

**Load sample cases** adds data without clearing existing work. Cases persist in `backend/nry.db` by default. For an isolated rehearsal, use the launcher option `--db /path/to/rehearsal.db` (a Windows path is also accepted), or set `NRY_DB` before starting uvicorn. **Reset demo** in `/demo` clears the selected database's saved work; it is not needed to view the dashboard.

Account evidence uses `NRY_NOW` (default `2026-11-15T12:00:00Z`), while waiting time uses the current clock. Leave the fixed evidence clock in place to reproduce the synthetic scenarios. [Architecture](docs/architecture.md) explains this distinction.

## Validation

From the root, with the Python environment active:

```bash
python tools/check_backend.py
```

The runner executes the existing suites separately and fails if any suite fails:

| Suite | Coverage |
|---|---|
| `prorio.selftest` | Score examples, gates, proposals, delivery dates and protocols |
| `test_api.py` | Case lifecycle, decisions, customer outcomes and errors |
| `test_db.py` | Persistence across real process restarts |
| `test_workspace.py` | Assets, staff/intake access controls and sample loading |
| `test_insights.py` | Metric reconciliation, ownership, clocks and context |
| `test_collaboration.py` | Claims, handoffs, stale writes, drafts and recovery |
| `test_clario_live.py` | Signed tools and customer-scoped fake sessions, without live calls |

Browser checks:

```bash
cd frontend
npm ci
npx playwright install chromium
npm test
```

Both browser suites start temporary servers and databases. They preserve the development queue and produce ignored screenshots/reports under `frontend/test-results/`. Set `BEACON_PYTHON` to your environment's Python executable if it differs from `backend/.venv/bin/python` (required on Windows); `BEACON_CHROMIUM` can select an installed Chromium. Default ports are 8025 and 8026; overrides are `BEACON_TEST_PORT` and `BEACON_COLLAB_PORT`.

[CI](.github/workflows/ci.yml) runs backend suites on Linux and Windows, plus browser checks and documentation-link validation on Linux. Local cleanup validation passed seven backend suites and 103 browser checks. Automated accessibility checks complement, rather than replace, manual officer and screen-reader evaluation.

For documentation-only checks: `python tools/check_docs.py`. For fresh portfolio captures, activate the same environment and run `node tools/capture-screenshots.cjs` after installing frontend development dependencies. The capture utility creates and removes its own temporary database.

## Optional live Clario

Follow [docs/live-services.md](docs/live-services.md) for the external Retell boundary and [LIVE_TEST_CHECKLIST.md](LIVE_TEST_CHECKLIST.md) for environment-specific validation. Never copy credentials into Git, screenshots or decks. Scripted mode works without them.

## Troubleshooting

- **Connection refused:** start the server on the computer where the browser runs and keep its terminal open. A cloud machine's localhost is not a public URL for your Windows browser.
- **Broken/stale logo:** current sidebar artwork is embedded SVG. Reload the current app; a cached earlier checkout may show the retired bank mark.
- **Empty queue:** load sample cases, or run a scripted scene and confirm its card.
- **Live mode returns 503:** live credentials/agent IDs are missing or invalid; use scripted mode or configure your own Retell account.
- **Conflicting decision:** refresh the case; another officer may own it or have changed its revision.

The separate legacy Streamlit console in `console/` is retained for history. `web/` is still active: it serves the current customer and demo pages.
