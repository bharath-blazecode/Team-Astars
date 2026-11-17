# Westpac SpeedQ: current build and delivery guide

This is the current runbook for the implemented dashboard and the presentation-slide submission video. It replaces
the original backend/Streamlit build brief. The [README](README.md) is the detailed product, API and roadmap reference.

**Source reviewed:** remote `main` at `3007368` on 17 Nov 2026 (Brisbane). PR #18 merged pale rose navigation,
#19 added automatic `.env` loading, #20 merged the [slide-video plan](docs/video/SHOT_LIST.md) and #21 made the demo
officer-first with an optional conversation preview from Live intake. This revision replaces the bank logo with
an original headset symbol. A merged software feature is separate from a completed live rehearsal or
finished video export.

## What is built

| Component | Current implementation |
|---|---|
| Officer workspace | Self-hosted HTML/CSS/JavaScript in `frontend/`: queue, preview, case review, evidence, context, insights, protocols and learning loop |
| Backend and Prorio | FastAPI in `backend/`; deterministic 0–100 scoring, protocol proposals, case decisions and audit history |
| Collaboration and intake | Exclusive officer claims, handoff notes, named completion, stale-revision protection, shared updates and durable unranked drafts |
| Customer experience | `/customer` and `/demo`: scripted fallback scenes and live Retell text/voice entry points |
| Persistence | SQLite cases, claims, drafts, audit events, mock account changes and protocol versions |
| Branding | Westpac SpeedQ name, original headset with one microphone, pale rose sidebar and restrained red actions; the bank logo is removed in this revision. See [BRANDING.md](BRANDING.md) |
| Submission video | Narrated presentation slides using diagrams and prototype screenshots; deck and export remain team deliverables |

The account data is synthetic: six customers, 31 transactions, six card records and 31 protocols. Account evidence
uses the fixed demo clock (`NRY_NOW`, default 15 Nov 2026, 12:00 UTC); waiting time uses the current clock. The legacy
Streamlit console is reference material, not the current dashboard.

## Run the local prototype

**Windows:** extract the complete project ZIP, install Python 3.12+ if needed and double-click
`START_WINDOWS.cmd`. The launcher installs the existing Python requirements into `.dashboard-venv`, starts the
loopback server and opens the scripted demo in your browser. Keep its terminal open. Both the dashboard and `/demo`
then run on your computer, normally on port 8010 (or the next free port shown by the launcher). A cloud machine's localhost is separate; opening its address directly on Windows does not connect to
that cloud server. See [the Windows quick start](README.md#windows-open-it-on-your-own-computer).

From the repository root, with Python 3.12 available:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000
```

Open:

| Route | Purpose |
|---|---|
| `http://localhost:8000/` or `/officer` | Current officer dashboard |
| `http://localhost:8000/customer` | Customer app and live Clario entry points |
| `http://localhost:8000/demo` | Full-width officer demo; optional customer preview from Live intake |
| `http://localhost:8000/docs` | Self-hosted API reference, under the staff access rules |

No frontend build or Node server is required. **Load sample cases** adds cases without clearing the queue. The
scripted demo needs no external AI key. Customer conversation controls stay in their own app or the optional
Live intake preview, not in the left column. Keep one backend worker: ownership and event coordination are process-local.
The default unauthenticated demonstration accepts loopback clients only; remote staff access requires the configured
staff accounts, HTTPS and an allowed hostname. See [settings](README.md#settings) for the actual controls and limits.

## Configure live Clario only when needed

Copy `backend/.env.example` to `backend/.env`, then fill in the Retell API key and verify the voice/chat agent IDs.
The backend reads simple `KEY=value` settings at startup; existing shell variables take precedence. The real `.env`
is ignored by Git. Keep credentials out of commits, slides, recordings and copied terminal output.

Retell also needs a reachable HTTPS tunnel, the actual tunnel hostname in `NRY_ALLOWED_HOSTS`, and correctly
configured signed tool calls. Restart the backend after changing settings. Follow
[LIVE_TEST_CHECKLIST.md](LIVE_TEST_CHECKLIST.md) for the complete setup, rehearsal and failure recovery. The
`/webhook/retell` final-card intake is a separate alternative and requires its intake secret for remote requests.
The documented transfer destination is fictional; a real phone handoff needs an authorised destination and a live test.

## Verify the current software

Run the backend suites from `backend` with its virtual environment active:

```bash
python -m prorio.selftest
python test_api.py
python test_db.py
python test_workspace.py
python test_insights.py
python test_collaboration.py
python test_clario_live.py
```

From the repository root, browser checks need Node 22.12+:

```bash
cd frontend
npm ci
npx playwright install chromium
npm test
```

The checks use isolated databases and retain the development queue. Browser tests cover the dashboard and customer
flows, two officer sessions, desktop/mobile layouts and automated accessibility rules. Clario tests use a faked
Retell client; passing them does not prove a live call, chat or phone transfer works. Manual officer usability and
screen-reader review remains open.

## Rehearsal acceptance checklist

Use a separate rehearsal database (`NRY_DB`) before **Reset demo**, which clears saved work in the selected database.

- [ ] Queue and preview show actual stored cases, priority reasons and concise customer context.
- [ ] Unconfirmed Live intake cards stay outside the ranked queue; confirmation submits the card once.
- [ ] An officer can review, approve/modify or handle manually, and the customer sees the recorded outcome.
- [ ] A second officer sees the claim/completion and cannot decide another officer's claimed case.
- [ ] Insights reconcile with saved cases; priority reasons and any score cap are visible.
- [ ] A suggestion is approved by a human before the active protocol version changes.
- [ ] The selected live Clario setup passes the [live checklist](LIVE_TEST_CHECKLIST.md), or the presentation clearly
      uses labelled screenshots from scripted scenes.
- [ ] The narration accurately describes synthetic data, simulated banking actions and any unverified integration.

## Make the presentation-slide video

Use [docs/video/SHOT_LIST.md](docs/video/SHOT_LIST.md) for the slide sequence, screenshot list, narration and export
checks. The production work is a deck, speaker notes, current screenshots and a recorded slide presentation. Confirm
competition duration/submission rules with the organisers; historical deadlines are not current instructions.

Keep a PDF of the deck and the exported video available as fallbacks. Use the original headset and fresh captures following [BRANDING.md](BRANDING.md),
and researched content follows [the source notes](backend/data/PROTOCOLS_SOURCES.md).

## Remaining work

- Finish the slide deck, narration, export and submission checks.
- Rehearse real Retell text/voice and the customer → officer → customer outcome on the demo machine.
- Replace older bank marks in the slide deck with the original headset, refresh captures and confirm separate content guidance and usability/accessibility feedback.
- Evaluate further dashboard ideas against officer needs; see [FEATURE_REVIEW.md](FEATURE_REVIEW.md).
- Treat SSO/MFA, role separation, shared state across workers and real bank integrations as production work beyond
  this prototype. Surge mode and additional workload/timeline/preference views remain candidates, not merged features.
