# Technical reference

Scoring, protocol, permission, API and configuration detail retained from the implementation documentation.
For the completed project overview and current setup, use the [README](../../README.md) and [BUILD](../../BUILD.md).
The priority thresholds and response targets below are project rules, not official banking SLAs. A band message such as “a specialist is joining” is prototype copy, not proof of a real transfer. “Verified” signals refer to owned synthetic account records. Permissions describe simulated or drafted actions; no production identity or biometric checks are implemented.

## How priority is worked out

### What counts as high and low

- **High priority:** money is leaving or about to leave, money was taken without consent, the customer cannot reach
  their own money, someone may be controlling the customer or the account right now, or the account's security is in
  question.
- **Low priority:** information or a routine service where nothing is at risk and nothing about security changes (a
  delivery date, a statement copy, a fee explanation, branch hours).
- **The trap: "looks simple, isn't safe."** Changing an address, phone number or email, adding a device, raising a
  limit, removing a block or giving another person authority over an account look like admin, but they are the first
  steps in an account takeover or financial abuse. These are always handled by an officer, at P3 or higher. ("Finding
  the address" is a safe read; "changing the address" is not.)
- **Safety cases.** Family violence, financial abuse and elder financial abuse can look like a hardship or admin
  request, but someone may be controlling the customer's money. They never sit below P2.
- **Asking is safe.** "Is this call or message really from Westpac?" is ranked as a general question, because checking
  is the behaviour we want to encourage and nothing is at risk yet. The moment the customer says they shared codes,
  installed something, moved money, or that the caller is still on the line telling them what to do, Clario switches
  to the scam path.

### The score (0 to 100)

```
Score = Harm (0-60) + Time to harm (0-20) + Verified account signals (0-20) + Care needs (0-10) + Waiting (0-10)
        capped at 100
```

**The score is computed by code, not by the language model.** Clario's model only classifies the issue type and
extracts cues; a backend function adds the points. For the same structured inputs, evidence, time and active protocol, scoring is deterministic and every point has a written reason.

| Harm (what is at stake) | Code in `protocols.json` | Points |
|---|---|---:|
| Scam in progress (told to move money, remote access, someone on the line) | `SCAM_IN_PROGRESS` | 60 |
| Unauthorised transaction (money taken without consent) | `UNAUTHORISED` | 45 |
| Locked out of own money, or suspected account takeover | `ACCOUNT_ACCESS` | 40 |
| Card lost or stolen | `CARD_LOST` | 35 |
| Payment missing (sent but not received, mistaken payment) | `PAYMENT_MISSING` | 35 |
| Financial hardship, or a safety case | `HARDSHIP` | 30 |
| Disputed charge (known merchant, wrong amount or service) | `DISPUTE` | 20 |
| Complaint about service | `COMPLAINT` | 15 |
| Service request (delivery, statement, address lookup) | `SERVICE` | 5 |
| General question | `GENERAL` | 0 |

The same codes and points are stored once in `backend/data/protocols.json` (`_about.harm_categories`), and every
protocol names the code it scores under. The scoring code reads the points from there. If a number changes,
change it there and in this table.

| Time to harm | Points |
|---|---:|
| Harm is happening now: money still leaving, scammer still in contact, repeated debits | +20 |
| Money may still be recoverable if acted on today (transaction under 72 hours old or still pending) | +10 |
| Neither | 0 |

| Verified account signal (+10 each, maximum +20; from account data only, never from the customer's words) |
|---|
| New payee added in the last 24 hours |
| Transfer much larger than usual (over $1,000, or over 3 times the customer's typical payment) |
| Password, device or contact details changed in the last 7 days |
| Card used somewhere unusual for this customer |
| Payee already appears in other open scam cards today (Prorio's cross-case check) |

| Care needs (+10 once) |
|---|
| Customer cannot pay for essentials (food, rent, medication), or shows vulnerability cues: distress, confusion, coaching, needs language support, an older customer struggling with digital steps |

| Waiting |
|---|
| +2 for every 10 minutes in the queue, maximum +10 |

### Bands

Response targets are Westpac SpeedQ design targets, not Westpac figures.

| Band | Score | Who handles | AI's job | Design target | Customer sees |
|---|---|---|---|---|---|
| **P1 Critical** | 80 to 100 | Fraud specialist, immediately | Clario has already offered SafeBlock or a card lock; Prorio drafts the recall and scam report | Warm handoff to the next available specialist, aim under 2 minutes | "A fraud specialist is joining now" |
| **P2 High** | 60 to 79 | Officer | Prorio drafts the full proposal | Within 30 minutes, or a booked callback | Position in queue, or callback time |
| **P3 Medium** | 40 to 59 | Officer | Prorio drafts the full proposal | Same business day | "With our team today", reference number |
| **P4 Low** | 0 to 39 | AI prepares, officer approves with one click | Prorio prepares the complete reply or action from the protocol | Same business day, usually minutes | Status updates, then the answer |

Routine questions can finish during intake. P4 cases include customers who still ask for an officer or need routine sign-off; no proportion of avoided calls is measured.

### Gates (they override the score)

| Gate | Rule |
|---|---|
| **G1 Words alone can't reach P1** | Without at least one verified account signal, the score is capped at 79 (P2) and flagged *"Customer reports scam, no account signals yet: officer to verify"*. Typing "scam" does not jump the queue. |
| **G2 Protect first** | Protect-first is the intended conversation flow. Proposals distinguish reported protection from synthetic account state; the prototype does not implement Face ID or independently prove an offer occurred before intake. |
| **G3 Security floor** | Any request that changes identity, contact details or devices, raises a limit, removes a lock or gives another person authority or access is officer-only and never below 40 (P3). |
| **G4 Ageing ceiling** | Waiting can lift a case by at most one band, with a maximum ten-point waiting contribution. This does not guarantee a maximum wait or eliminate starvation. |
| **G5 Officer override** | An officer can re-rank any case with a reason; it is logged and reviewed. |
| **G6 One problem, one card** | Repeat contacts about the same issue update the existing card instead of creating new ones. |
| **G7 Safety floor** | Family violence, financial abuse and elder financial abuse are never below 60 (P2), in the configured protocols. Specialist referrals and safe-contact handling remain protocol intent and simulated actions, not verified real-world service delivery. Words alone can reach P2 here, never P1 (G1 still applies): a false claim costs an officer a few minutes, but a missed one can cost someone their safety. |

### Worked examples (synthetic customers)

| Case | Calculation | Score and band |
|---|---|---|
| **Maria:** "Someone from the bank told me to move my savings"; $4,800 to a new payee 2 hours ago | Scam 60 + happening now 20 + new payee 10 + large transfer 10 | **100, P1** |
| Same words, but no unusual activity on the account | Scam 60 + happening now 20 = 80, capped by G1 | **79, P2**, "officer to verify" |
| **Priya:** $89 "SP DIGITALHUB SUBS" that isn't hers (after Clario first shows her the merchant details) | Unauthorised 45 + recoverable 10 | **55, P3**; card lock offered at once (G2) |
| Priya, and the card was also used overseas yesterday | 55 + unusual location 10 | **65, P2** |
| **Minh:** $650 rent sent by Osko, landlord says not received, prefers Vietnamese | Payment missing 35 + recoverable 10 + care (rent, language) 10 | **55, P3** |
| Locked out after a password change from a new phone, can't buy groceries | Locked out 40 + device change 10 + care 10 | **60, P2** |
| Lost job, can't make the home loan payment | Hardship 30 + care 10 | **40, P3**, officer-led (hardship is a regulated assessment) |
| **Sam:** "When is my new card arriving?", not satisfied after Clario's answer | Service 5 | **5, P4**, AI prepares, officer approves |
| "Please change my address" | Service 5, raised by G3 | **40, P3**, officer-only |
| "I want my daughter to be able to help with my banking" | Service 5, raised by G3 | **40, P3**, officer-only; Clario first checks the choice is the customer's own |
| "My son keeps taking money from my account and I'm scared to say no" | Hardship 30 + care 10 = 40, raised by G7 | **60, P2**, specialist team |
| "Is this text really from Westpac?" (nothing shared, nothing moved) | General 0 | **0, P4**, Clario answers at Tier 2 and checks for a genuine bank contact on file |
| Same question, but "they're still on the phone and want my code" | Switches to scam in progress: Scam 60 + happening now 20 = 80, capped by G1 unless account signals back it | **79, P2** (or P1 with signals), SafeBlock offered first |

### Why this holds up

- It ranks by harm and recoverability, which is how fraud teams already think: minutes matter while money can still be
  stopped.
- Account evidence outweighs words, so it is hard to game, and a gamed case still lands with an officer, not an AI.
- Vulnerability gets a boost, but a capped one (+10), so it helps without overriding real emergencies.
- It is **designed to support** the complaint and hardship response timeframes in ASIC RG 271 and the
  detect-and-disrupt expectations of the Scams Prevention Framework. It is a prototype; we do not claim compliance.

---

## Who may do what

These are the implemented prototype boundaries. The original product-vision permission matrix is retained only in the [historical README](../archive/README.md#who-may-do-what).

| Component | Implemented responsibility | Boundary |
|---|---|---|
| Clario adapter | Customer-scoped lookup, draft updates, confirmation and corrections through signed tools | Selected synthetic customer context; not production identity verification |
| Prorio | Read structured fields, gather owned evidence, score and draft a protocol response | No language model; free-text summaries do not enter the ranker; no real bank operations |
| Officer workspace | Inspect context, claim/release, approve/modify/manual decisions and record outcomes | Server checks ownership/revisions; Basic accounts do not implement production role separation |
| Protocol review | Record suggestions, approve versions and roll back | A human initiates approval; the prototype has no separate protocol-owner authorisation role |
| Customer status | Show case progress and recorded result without exposing the numeric priority score | Demonstration access is not a production customer login |

The API lookup does not expose balances to live Clario; officer case context can show the case customer's masked account evidence. Banking actions use the fixed mocked action list. Callback, recall, report, protection and message records are simulations or drafts; no refund, payment, real card lock, real biometric check or live bank commitment is performed.

### Structured input boundary

`backend/prorio/agent.py` copies issue type, customer/case IDs, linked transaction IDs, allowed caller cues, language and reported protection state. Free-text summaries are excluded. The evidence layer ignores transactions not owned by the case customer.

This prevents instructions in summary text from directly changing deterministic ranking. It is not a claim of complete prompt-injection resistance: conversational classification and structured signals still depend on the intake path and service configuration.

## The Customer Service Card

Intake drafts hold the developing need, structured facts and reported protection separately from backend-derived evidence. A draft stays outside the operational queue until confirmation. The scripted flow confirms explicitly; live Retell confirmation relies on the signed agent tool call after its read-back. The backend cannot independently establish real-world consent or identity from that call.

Customer corrections update the associated open case under the supported correction path. Prorio appends score reasons and a proposed response; the officer explicitly picks up the case and decides what to do. The customer-facing status omits the numeric score. [Demo guide](../demo.md) shows Maria's escalation and Sam's P4 request for an officer.

## The Protocol Database and the learning loop

For the demo, the Protocol Database is [`backend/data/protocols.json`](../../backend/data/protocols.json): **31 protocols**,
one per issue type, written in our own words from public sources. Each protocol lists its sources, and steps marked
`team_design` are our own design, not a published rule. It is **not** Westpac's internal procedure.
[`PROTOCOLS_SOURCES.md`](../../backend/data/PROTOCOLS_SOURCES.md) explains how it was built and the copyright rules for
changing it.

One entry, shortened (the `clario_can_answer` list is cut to one item):

```json
{
  "issue_type": "CARD_DELIVERY",
  "title": "When will my card arrive?",
  "version": "2.0", "harm_category": "SERVICE", "min_band": null,
  "clario_can_answer": ["Answer from card tracking: dispatched, carrier, status, expected date."],
  "protect_first": null,
  "steps": [
    {"who": "AI (Clario)", "step": "Answer from tracking data", "source": "team_design"},
    {"who": "AI (Prorio)", "step": "If past the expected date, prepare a replacement to the address on file", "source": "team_design"},
    {"who": "officer", "step": "One-click approve (P4)", "source": "team_design"}
  ],
  "ai_may": ["prepare ORDER_REPLACEMENT_CARD", "SEND_CUSTOMER_UPDATE"],
  "officer_must": ["approve the replacement"],
  "required_checks": ["address changes go to DETAILS_CHANGE"],
  "customer_message": "Your card was sent on {dispatched} and should arrive by {expected}. You can use your digital card in the app until then.",
  "timeframes": []
}
```

| Field | Meaning |
|---|---|
| `harm_category` | Which row of the harm table the case scores under |
| `min_band` | A gate: the lowest band the case may sit in (`null` means the score decides) |
| `clario_can_answer` | What Clario may tell the customer straight away (Tier 1 or 2) |
| `protect_first` | The protective action offered before queuing (G2), always the customer's choice |
| `steps` | Who does what, in order: customer, AI (Clario), AI (Prorio) or officer, each with a source |
| `ai_may` / `officer_must` | What the AI may prepare or do, and what only a person may decide |
| `required_checks`, `customer_message`, `timeframes`, `sources` | Checks before acting, the reply template, sourced timeframes, and links |
| `change_log` | What changed in each version and why |

**All 31 issue types, by harm category** (a gate is shown where the protocol sets a minimum band):

| Harm code | Points | Issue types |
|---|---:|---|
| `SCAM_IN_PROGRESS` | 60 | `SCAM_IN_PROGRESS` |
| `UNAUTHORISED` | 45 | `SCAM_ALREADY_PAID`, `FRAUD_UNAUTHORISED`, `UNAUTHORISED_ONLINE_BANKING` |
| `ACCOUNT_ACCESS` | 40 | `IDENTITY_THEFT` (G3, P3+), `ACCOUNT_ACCESS` (G3, P3+), `ACCOUNT_RESTRICTED_ID_CHECK` (G3, P3+) |
| `CARD_LOST` | 35 | `CARD_LOST_STOLEN` |
| `PAYMENT_MISSING` | 35 | `MONEY_MISSING`, `BPAY_MISTAKE` |
| `HARDSHIP` | 30 | `HARDSHIP`, `FAMILY_VIOLENCE_FINANCIAL_ABUSE` (G7, P2+), `ELDER_FINANCIAL_ABUSE` (G7, P2+), `BEREAVEMENT`, `GAMBLING_HARM` |
| `DISPUTE` | 20 | `DISPUTE_CHARGE` |
| `COMPLAINT` | 15 | `COMPLAINT` |
| `SERVICE` | 5 | `LOGIN_HELP`, `DETAILS_CHANGE` (G3, P3+), `PAYMENT_LIMIT_CHANGE` (G3, P3+), `CARD_DECLINED`, `CARD_DELIVERY`, `CARD_ACTIVATION`, `PENDING_TRANSACTION`, `DIRECT_DEBIT_STOP`, `PAYID_ISSUE`, `TRUSTED_PERSON_ACCESS` (G3, P3+), `ACCOUNT_CLOSURE`, `OUTAGE_INCIDENT` |
| `GENERAL` | 0 | `VERIFY_CONTACT`, `GENERAL_ENQUIRY` |

Some protocols switch a case to another one when the facts change: `VERIFY_CONTACT` becomes `SCAM_IN_PROGRESS` as
soon as anything is at risk, `PENDING_TRANSACTION` is routed to a fraud, dispute or scam protocol, and
`TRUSTED_PERSON_ACCESS` becomes `ELDER_FINANCIAL_ABUSE` if the customer is being pressured.

**Officers teach, leads approve.** An officer's Modify or Manual decision becomes a protocol *suggestion*, not a rule.
When the same change has been suggested several times (for example 3), it is offered to a protocol owner (a team lead)
who approves or rejects it. Every protocol has a version number, every proposal shows which version it used, every
change is recorded in the protocol's `change_log`, and any change can be rolled back. The protocols start at v2.0; the
four changed after the team's review are at v2.1. In the demo, an officer modifies a proposal and it appears as the
next version, "pending approval".

---

## The demo customers

Six made-up customers. Data lives in `backend/data/` (`customers.json`, `transactions.json`, `cards.json`).

| ID | Name | Situation | Expected under Westpac SpeedQ |
|---|---|---|---|
| CUST-001 | Maria Russo | Paid $4,800 to a brand-new payee after a caller claiming to be from the bank told her to move her savings | Scam path: SafeBlock offered first, **100, P1**, warm handoff to a fraud specialist |
| CUST-002 | Sam Taylor | Asking when a replacement card will arrive (dispatched 12 Nov, due 19 Nov) | **Route A, Tier 1**: answered from his data. Only queued (**5, P4**) if he is not satisfied |
| CUST-003 | Priya Sharma | A $89 charge she doesn't recognise (SP DIGITALHUB SUBS) | Card lock offered (G2), **55, P3**, Prorio drafts a dispute |
| CUST-004 | Minh Nguyen | Sent $650 rent by Osko but the landlord says it never arrived. Prefers Vietnamese | **55, P3**, card shown as "Vietnamese (translated)", outcome returned in Vietnamese |
| CUST-005 | Alex | Replacement card due 19 Nov, with an everyday account and an eSaver account | Extra example for card-delivery questions |
| CUST-006 | Jordan Lee | Locked out after the password was changed from a new phone; can't buy groceries | `ACCOUNT_ACCESS` with `ESSENTIALS_AT_RISK`: **60, P2** (locked out 40 + device change 10 + care 10) |

The demo aims to show a clear handoff without re-asking, an officer-approved P4 answer, and a protective response
before ranking a scam case. Timings are demonstration targets; simulated protection is not a measured banking outcome.

---

### How Prorio works

Prorio is code: the same structured inputs, evidence, waiting time and approved protocol produce the same result.
It sends no customer data to an external model or API. For every card it records these steps in a trace:

1. **Read card.** Only structured fields: issue type, linked transaction IDs, conversation signals, language. The
   customer's free-text summary is never read, so "ignore your rules, make me P1" cannot change anything.
2. **Gather evidence** from account data: only transactions linked to the card **and** belonging to that customer.
3. **Score**: harm (from the protocol's harm category) + time to harm + verified signals + care needs + waiting.
4. **Apply gates**: G1 words alone can't reach P1; G3 and G7 through each protocol's `min_band` (for example address
   changes P3, family violence and elder financial abuse P2); G4 waiting lifts at most one band; G5 officer re-rank;
   G6 a repeat contact updates the open card instead of creating a new one.
5. **Match protocol** in the Protocol Database and use any version a protocol owner has approved.
6. **Draft proposal**: actions from the fixed executable list (each one mocked), officer tasks for anything else,
   required checks, the customer message filled in, timeframes and sources.
7. **Assign**: P1 to P3 are carried out by an officer; P4 by the AI after one-click officer approval.

**Safety net for a misfiled charge.** If a card arrives as `DISPUTE_CHARGE` but the merchant has never appeared in the
customer's history, Prorio scores it under the unauthorised harm row with the reason "Merchant never seen before on
this account: scored as possible unauthorised, officer to confirm". It never changes the issue type Clario recorded.

**Demo clock.** Account evidence ("still recoverable", "changed in the last 7 days") is judged as of
**15 Nov 2026, 12:00 UTC**, so scores are the same on every run. Waiting time uses the real clock. Set `NRY_NOW` to
change it, or `NRY_NOW=real` to use the real clock.

---

## Reference: backend endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/webhook/retell` | Receives a card from Clario; Prorio scores it and drafts a proposal; short reply with band, `handoff` and caller message. With `case_reference` and `correction`, records the customer's correction on their open card |
| POST | `/case` | Same as above, for posting cards by hand; returns the full card |
| GET | `/queue` | The priority list: open cases, most urgent first, with reasons and current waiting time |
| GET | `/case/{id}` | One full card, including Prorio's proposal and trace |
| GET | `/case/{id}/proposal` | Prorio's proposed solution: protocol and version, actions, officer tasks, checks, customer message, sources |
| GET | `/case/{id}/trace` | What Prorio did, step by step |
| GET | `/case/{id}/status` | The customer's view: Received, Ranked, With an officer, Action taken, Done, and the outcome. No score |
| POST | `/case/{id}/pickup` | Claim an active case exclusively; accepts `expected_revision`. Authenticated identity determines the owner; the customer sees "With an officer" |
| POST | `/case/{id}/decision` | `{"decision": "APPROVE" \| "MODIFY" \| "MANUAL", "actions": [...], "officer": "name", "note": "...", "suggest_update": true}` |
| POST | `/case/{id}/complete` | Close a Manual case: `{"note": "what was done"}` (sent to the customer) |
| POST | `/case/{id}/rerank` | `{"band": "P1", "reason": "..."}` or `{"score": 90, "reason": "..."}` (0 to 100). Reason required |
| GET | `/audit/{id}` | The audit log for a case |
| GET | `/protocols` | Every protocol with its version, harm category, minimum band and decision counts |
| GET | `/protocols/{issue_type}` | One protocol as Prorio uses it, with approved changes and sources |
| POST | `/protocols/{issue_type}/rollback` | Undo the latest approved version |
| GET | `/suggestions` | Protocol suggestions from officers' Modify and Manual decisions |
| POST | `/suggestions/{id}/approve` | Protocol owner approves (only once it has been suggested enough times); creates a new version |
| POST | `/suggestions/{id}/reject` | Protocol owner rejects |
| GET | `/meta` | Fixed lists for the dashboard: actions, bands, issue types, demo clock |
| GET | `/` | The same-origin officer dashboard |
| GET | `/workspace/session` | Current staff identity and local demo status; never credentials |
| GET | `/workspace/cases` | Compact active, manual and completed case list |
| GET | `/workspace/insights` | Read-only analytics across saved cases; ownership-checked payment totals and live response watch |
| GET | `/workspace/intake` | Active unranked drafts and the five latest confirmed handoffs |
| GET | `/workspace/events` | Authenticated same-origin server-sent invalidations; clients re-fetch snapshots |
| POST | `/intake/drafts` | Start a customer intake draft, separate from the ranked queue |
| GET / POST | `/intake/drafts/{id}` | Read or update a draft using its expected revision |
| POST | `/intake/drafts/{id}/confirm` | Confirm and submit a reviewed draft once; retries reuse its case |
| POST | `/intake/drafts/{id}/cancel` | Cancel an unsubmitted draft using its expected revision |
| POST | `/case/{id}/release` | Assigned officer returns active work to the shared queue with an optional note |
| GET | `/case/{id}/context` | Masked records belonging to this case's customer, reported/verified protection and evidence-clock history |
| POST | `/demo/seed` | Add synthetic examples once, preserving existing work; local demo mode only |
| POST | `/clario/session/chat`, `/clario/session/call` | Customer app: start a live Retell chat or browser call for the signed-in customer (local only) |
| POST | `/clario/session/chat/{chat_id}` | Customer app: send a chat message to Clario; returns Clario's replies and the card reference once filed |
| GET | `/clario/session/{conversation_id}` | Customer app: the card reference and draft for a live conversation |
| POST | `/retell/tools/{name}` | Clario's Retell custom functions (`lookup_customer`, `update_card`, `submit_card`, `correct_card`); Retell-signed |
| GET | `/clario/{customer_id}/lookup` | Clario's read-only look-up for the signed-in customer: first name, masked accounts, card delivery, payees, recent transactions. No balances |
| GET | `/demo`, `/officer`, `/customer` | Recording demo, redesigned officer workspace and retained customer app |
| POST | `/admin/reset` | Rehearsal reset: clears cases, drafts, mock account changes, suggestions and approved versions; inherits staff authentication/local-only access |

Case claims, releases, decisions, manual completions and re-ranks accept an optional `expected_revision`; the current
dashboard always supplies it. Draft updates, confirmation and cancellation require it. Ownership checks apply even
to legacy case clients that omit a revision. A second officer must wait for release before acting on claimed work.

Errors include `401` missing/invalid credentials or intake secret, `403` denied origin/access, `404` not found,
`409` ownership/revision conflict, already decided or not ready, `422` invalid request, and `503` missing required
intake-secret configuration. Searchable, self-hosted API/schema reference: `http://localhost:8000/docs` while
the backend runs. The OpenAPI document is at `/openapi.json`.

Executable actions (all mocked, they only record that they happened): `ACTIVATE_SAFEBLOCK`, `BLOCK_CARD`,
`RAISE_DISPUTE`, `DRAFT_PAYMENT_RECALL`, `DRAFT_PAYMENT_TRACE`, `DRAFT_SCAM_REPORT`, `DRAFT_HARDSHIP_NOTES`,
`DRAFT_COMPLAINT_RESPONSE`, `ORDER_REPLACEMENT_CARD`, `BOOK_CALLBACK`, `SEND_CUSTOMER_UPDATE`, `SEND_GUIDE_LINK`,
`REFER_SPECIALIST_TEAM`. Drafts are always drafts, and money is never moved.

---

## Where data is kept

- **Customer data** (accounts, transactions, cards) is read from `backend/data/` on every start.
- **Cases** are saved in a small **SQLite** file, `backend/nry.db`, created on first start and not committed to git.
  Cases, audit logs, claims/revisions, intake drafts, re-ranks, mocked account changes, protocol suggestions and approved
  protocol versions survive a restart. `protocols.json` itself is never written by code.
- To empty it for rehearsal, use **Reset demo** on `/demo` or the protected `POST /admin/reset`. Set `NRY_DB` to use a separate file.

---

## Settings

All optional environment variables. (The `NRY_` prefix is left over from the earlier project name.)

| Variable | Default | Used by | Meaning |
|---|---|---|---|
| `NRY_API` | `http://localhost:8000` | Legacy Streamlit only | Backend address; the current dashboard uses same-origin requests |
| `NRY_OFFICER` | `Demo officer` (`officer` in Streamlit) | Backend local demo / legacy console | Default demo audit name. Authenticated accounts determine their own identity; the current local dashboard can simulate per-tab officers |
| `NRY_DB` | `backend/nry.db` | Backend | Where the database file lives |
| `NRY_WEBHOOK_SECRET` | unset (local demo only) | Backend | Required for remote or staff-authenticated intake; protects `/webhook/retell`, `/case` and draft writes with `x-webhook-secret` |
| `NRY_NOW` | `2026-11-15T12:00:00Z` | Backend | The demo clock for account evidence. `real` uses the real clock |
| `NRY_SUGGEST_THRESHOLD` | `3` | Backend | How many times a protocol suggestion must be made before the owner can approve it. Set `1` for a quick demo |
| `NRY_CORS_ORIGINS` | none | Backend | Comma-separated web origins allowed to call the API from a browser. Not needed: the pages are served by the backend itself |
| `NRY_STAFF_PASSWORD` | unset | Backend / dashboard | Enables HTTP Basic staff authentication for the dashboard, staff APIs, docs and administration. Use a strong secret and HTTPS for remote access; never commit it |
| `NRY_STAFF_USER` | `officer` | Backend / dashboard | Staff username for the single-account password option; used in authenticated audit records |
| `NRY_STAFF_ACCOUNTS` | unset | Backend / dashboard | Secure JSON mapping of usernames to distinct passwords for prototype staff accounts. Takes precedence over the single account; invalid configuration fails closed. Never commit values |
| `RETELL_API_KEY` | unset | Backend | Starts live Clario sessions and verifies Retell's signed tool requests. Without it, live Clario returns `503`. Never commit it |
| `RETELL_VOICE_AGENT_ID`, `RETELL_CHAT_AGENT_ID` | unset | Backend | The Clario voice and chat agents in Retell |
| `NRY_ALLOWED_HOSTS` | `localhost,127.0.0.1,[::1],testserver` | Backend | Comma-separated hostnames accepted by the server. Add the actual hostname when placing the application behind an HTTPS proxy; avoid wildcards |

Without configured staff accounts or a staff password, staff access is restricted to loopback clients. Secret-authenticated intake can still be
used by a server-to-server voice integration. Remote intake and intake in staff mode require `NRY_WEBHOOK_SECRET` to be
configured; an unset secret fails closed. The browser never receives either secret. Cross-origin browser mutations
are rejected unless their origin is explicitly trusted through `NRY_CORS_ORIGINS`; unrestricted CORS has been removed, and the website uses a strict self-only Content Security Policy,
frame protection, no-store responses and text-only rendering of API data.

Distinct Basic accounts can be configured for prototype officers, but this is not production banking authentication:
it has no SSO, MFA, protocol-owner role separation or session revocation. The local demo identity selector is hidden
when authentication is enabled. Use synthetic data only. See [the interface design and security notes](../../DESIGN.md).

---

## Tests

The root runner `python tools/check_backend.py` executes all seven suites. Individual commands below run from `backend` with its environment active. Browser checks and CI setup are documented in [BUILD.md](../../BUILD.md#validation).

| Command | What it checks |
|---|---|
| `python -m prorio.selftest` | Every worked example in "How priority is worked out", the gates, the cross-case check, the firewall (summaries are ignored), and that all 31 protocols produce a proposal |
| `python test_api.py` | The whole backend through its endpoints: priority order, `handoff` reply, one problem one card, decisions, the P4 AI action, the customer status tracker, the learning loop, re-ranking and error cases |
| `python test_db.py` | Restarts the backend for real and checks nothing was lost, including approved protocol versions |
| `python test_workspace.py` | Website assets, local-only demo access, staff authentication, protected intake, audit identity, origin/host checks and additive sample loading |
| `python test_insights.py` | Empty and populated analytics, payment deduplication, customer ownership, clocks, stages, response-watch boundaries and context access control |
| `python test_clario_live.py` | Retell signatures, conversation-scoped customer, draft → ranked card, corrections, faked chat/call sessions, tunnel restrictions and `.env` loading without overriding existing variables; no real calls |
| `python test_collaboration.py` | Concurrent claims and decisions, transfers, stale revisions, authenticated identity, draft validation, retry safety and restart recovery |

The API/workspace tests use an in-memory database; persistence checks use a temporary file. They never touch `nry.db`.

Browser regression checks (Node 22.12+; development dependencies only):

```bash
cd frontend
npm ci
# If Chromium is not installed: npx playwright install chromium
npm test
```

Both browser suites start their own backend and temporary database, use installed Chromium when available, and check
the real UI: filtering, pickup, cancellation, approval, modified actions, manual outcomes, re-ranking, protocol changes,
hostile content, connection failures, chart drill-downs, score caps, customer context, handoffs, responsive layouts and automated WCAG accessibility checks. Screenshots and
accessibility reports (including checks requiring manual review) are written to ignored `frontend/test-results/`.
Set `BEACON_CHROMIUM` to choose another Chromium executable, `BEACON_PYTHON` for the backend Python executable, or
`BEACON_TEST_PORT` if its default port 8025 is occupied.
The collaboration suite uses port 8026 (`BEACON_COLLAB_PORT` overrides it), two independent officer sessions and the
actual customer scene. Checks include the full-width demo, optional preview, keyboard focus return, mobile fit,
separate customer tab and continued handoff while the preview is closed.

---
