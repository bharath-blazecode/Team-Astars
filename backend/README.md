# Backend (Clario intake + Prorio)

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

This also serves the officer dashboard at `http://127.0.0.1:8000`. No frontend build or separate UI process is
needed. **Load sample cases** adds a synthetic queue without resetting existing work. The old Streamlit dashboard
is optional. The API/schema reference at `/docs` is self-hosted and follows the same staff access controls.

**Status reviewed 17 Nov 2026 (Brisbane):** backend case handling, Prorio, persistence, care insights, shared officer
claims and live intake are implemented on `main`. Westpac SpeedQ branding and the local GEL mark are merged through
PR #14, verified at `60adbde`. This remains a single-worker prototype.
The current status and remaining dashboard/integration work are tracked in the
[main README](../README.md#remaining-work-and-next-iterations); the external Retell configuration is not stored here.

Checks: `python -m prorio.selftest` (Prorio's scoring, gates and proposals), `python test_api.py` (the API end to end),
`python test_db.py` (persistence across a restart), `python test_workspace.py` (dashboard integration and security).
`python test_insights.py` covers the analytics, customer scope, payment totals and evidence/live-clock boundaries.
`python test_collaboration.py` covers officer claim races, ownership transfer, stale decisions, identity, drafts and restart recovery.
Browser tests: `cd ../frontend && npm ci && npm test` (Node 22.12+ and Chromium). All customer data is synthetic.

Staff endpoints reject remote clients in local demo mode. Set `NRY_STAFF_PASSWORD` and optionally `NRY_STAFF_USER`
to enable Basic authentication, and use HTTPS for remote connections. Set `NRY_ALLOWED_HOSTS` to the intended hostname.
In this mode, configure `NRY_WEBHOOK_SECRET` for intake; the browser never receives these secrets. Basic authentication
is a prototype control, not production SSO or role-based authorisation. See `../DESIGN.md` for boundaries.

`NRY_STAFF_ACCOUNTS` optionally supplies a secure JSON mapping for distinct authenticated officers. The server uses
that account identity for claims and decisions. Local-only demo identity switching does not grant remote access and
is ignored in authenticated mode. Keep a single backend worker: the claim lock and SSE revision counter are process-local.

`GET /workspace/events` invalidates staff snapshots after changes. `GET /workspace/intake` lists unranked drafts.
The draft start/update/confirm/cancel routes use the same intake secret policy as the existing webhook. Confirmation
creates a ranked case only after the customer confirms; a persisted internal association protects retries. Existing
intake clients can keep using the final-card webhook. Modern officer clients should supply `expected_revision` on
claims and mutations; ownership and already-decided checks also protect legacy clients that omit this optional field.

`GET /workspace/insights` aggregates the saved workspace under the case-store lock. It does not reset cases or execute
actions. `GET /case/{id}/context` returns masked accounts and owned transactions for that case's customer, with the
fixed evidence clock and a separate current snapshot time. Both endpoints inherit staff access control. See
[FEATURE_REVIEW.md](../FEATURE_REVIEW.md) for metric definitions and limits.

## Prorio

`prorio/` is the Priority and Protocol agent. It is plain, deterministic code: no language model and no outside API.
It sends no data to an external model. See "How Prorio works" in the top-level README. Scores are judged against a
fixed demo clock (`NRY_NOW`, default 15 Nov 2026 12:00 UTC); waiting time uses the real clock.

## Database

SQLite (`backend/nry.db`, stdlib, created on first run, git-ignored). Cases and their audit logs, officer claims and
revisions, intake drafts, mock account changes (SafeBlock, blocked cards, draft reference counters), protocol suggestions
and approved protocol versions survive a backend restart. It is a single connection behind a lock: fine for a demo, not for concurrent production
writers. Pre-Prorio case records are skipped on start; current older case records acquire ownership/revision defaults
from their audit history where available.

For a clean rehearsal, `curl -X POST localhost:8000/admin/reset` or **Reset demo** on `/demo` clears cases, drafts,
mock changes, suggestions and approved versions. The endpoint inherits staff authentication and local-only demo
access; authenticated requests require staff credentials. The current dashboard has no reset button.
`NRY_DB=/path/x.db` points at a different file.

## Trigger the demo without Clario

Same body works on `/case` (testing, returns the full card) and `/webhook/retell` (Clario, returns a short reply).
These examples assume unauthenticated loopback demo mode. Configured intake secrets must be sent in
`x-webhook-secret`; remote or staff-authenticated intake requires the secret to be configured.

```
# Sam: card delivery answered by Clario. Stored, NOT in the queue
curl -s localhost:8000/case -H 'content-type: application/json' -d '{"customer_id":"CUST-002","customer_name":"Sam T.","issue_type":"CARD_DELIVERY","status":"TIER1_RESOLVED","summary_en":"Card dispatched 12 Nov, due 19 Nov"}'

# Sam, not satisfied -> 5, P4 (AI acts after one-click approval). Use CUST-005 for a second one
curl -s localhost:8000/case -H 'content-type: application/json' -d '{"customer_id":"CUST-002","customer_name":"Sam T.","issue_type":"CARD_DELIVERY","status":"QUEUED","summary_en":"Card not here yet; wants help"}'

# Priya: $89 charge she didn't make, card locked during the chat -> 55, P3
curl -s localhost:8000/case -H 'content-type: application/json' -d '{"customer_id":"CUST-003","customer_name":"Priya S.","issue_type":"FRAUD_UNAUTHORISED","linked_transactions":"TX-7001","card_locked":true,"summary_en":"$89 charge I did not make"}'

# Minh: missing $650 rent, Vietnamese -> 55, P3
curl -s localhost:8000/case -H 'content-type: application/json' -d '{"customer_id":"CUST-004","customer_name":"Minh N.","issue_type":"MONEY_MISSING","language":"vi","language_label":"Vietnamese","linked_transactions":"TX-8001","summary_en":"Missing $650 rent payment","summary_customer_lang":"Mất khoản tiền thuê nhà $650"}'

# Jordan: locked out after a password change from a new phone, can't buy groceries -> 60, P2
curl -s localhost:8000/case -H 'content-type: application/json' -d '{"customer_id":"CUST-006","customer_name":"Jordan L.","issue_type":"ACCOUNT_ACCESS","risk_signals":"ESSENTIALS_AT_RISK","summary_en":"Locked out after a password change I did not make"}'

# Maria: scam in progress -> 100, P1, jumps to the top; reply says WARM_TRANSFER_FRAUD
curl -s localhost:8000/webhook/retell -H 'content-type: application/json' -d '{"customer_id":"CUST-001","customer_name":"Maria R.","issue_type":"SCAM_IN_PROGRESS","linked_transactions":"TX-9001","risk_signals":"CUSTOMER_REPORTS_PRESSURE,VULNERABILITY_CUES","safeblock_activated":true,"summary_en":"Caller says someone claiming to be from Westpac told her to move her savings.","case_reference":"WGM-0412"}'

# Bare scam claim, nothing on the account -> 79, P2, "officer to verify" (gate G1)
curl -s localhost:8000/case -H 'content-type: application/json' -d '{"customer_id":"CUST-002","issue_type":"SCAM_IN_PROGRESS","risk_signals":"CUSTOMER_REPORTS_PRESSURE"}'

curl -s localhost:8000/queue
```

## Officer actions

Use the current dashboard for the complete claim/review workflow. The API also supports `/pickup` and `/release`;
only the assigned officer may change a claimed case. Current clients should send `expected_revision` from the last
case read on every mutation. Staff authentication determines the audit actor, regardless of a body-supplied name.
The examples below are local-demo calls on unclaimed cases; substitute current references and the owning identity
when following up work already claimed or decided.

```
# what Prorio proposes, and what it did
curl -s localhost:8000/case/WGM-0412/proposal
curl -s localhost:8000/case/WGM-0412/trace

# approve (APPROVE), run an edited list (MODIFY, becomes a protocol suggestion), or handle it yourself (MANUAL)
curl -s localhost:8000/case/WGM-0412/decision -H 'content-type: application/json' -d '{"decision":"APPROVE","officer":"j.officer"}'
curl -s localhost:8000/case/WGM-0900/decision -H 'content-type: application/json' -d '{"decision":"MODIFY","officer":"j.officer","note":"Customer wants a new card","actions":[{"action":"SEND_CUSTOMER_UPDATE"},{"action":"ORDER_REPLACEMENT_CARD"}]}'

# re-rank: exactly one of band / score (0-100), reason required, logged. The score is then pinned
curl -s localhost:8000/case/WGM-0901/rerank -H 'content-type: application/json' -d '{"band":"P1","reason":"Customer is vulnerable"}'

# the customer's view of their card (no score)
curl -s localhost:8000/case/WGM-0412/status
curl -s localhost:8000/audit/WGM-0412
```

## Learning loop

```
curl -s localhost:8000/suggestions
curl -s localhost:8000/suggestions/SUG-0001/approve -H 'content-type: application/json' -d '{"owner":"team lead"}'
curl -s localhost:8000/protocols/FRAUD_UNAUTHORISED
curl -s localhost:8000/protocols/FRAUD_UNAUTHORISED/rollback -H 'content-type: application/json' -d '{"owner":"team lead"}'
```

A suggestion can be approved once it has been made `NRY_SUGGEST_THRESHOLD` times (default 3; set 1 for a quick demo).
