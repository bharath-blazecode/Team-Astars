# Feasibility review: make the existing data useful

The implemented dashboard keeps the priority queue as its first screen; **Care insights** offers a graphical route
into the work. Shared ownership and **Live intake** extend the handoff while retaining human approval.

**Reviewed 17 Nov 2026 (Brisbane)** against `main` at `60adbde`: insights/context were merged in PR #9,
collaboration/live intake in PR #10, and Westpac SpeedQ branding in PR #14. The original dashboard partitions remain
in place. Further brainstorming, appearance refinement and manual usability review are
still planned. The [README roadmap](README.md#remaining-work-and-next-iterations) is the current work checklist.

## What is actually available

| Source | Records | Useful facts | Limits |
|---|---:|---|---|
| `backend/data/customers.json` | 6 | Masked accounts, balances, language, payees, security and lockout events | Synthetic snapshots; not live banking feeds |
| `backend/data/transactions.json` | 31 | Owner, amount, payee, timestamp and transaction type | Not labelled fraud outcomes; not a representative behavioural history |
| `backend/data/cards.json` | 6 | Current/mock block state and replacement delivery milestones | Expected delivery is not proof of arrival |
| `backend/data/protocols.json` | 31 protocols | Harm points, minimum bands, checks, actions and sources | Procedures do not establish that checks occurred in real life |
| Saved case and audit records | Varies by local workspace | Current stages, scores, score parts, decisions, pickup history, repeat contacts and protocol suggestions | Small demonstration history; case creation uses the live clock |
| Case assignments/revisions and intake drafts | Varies by local workspace | Current officer, claim/release/completion events, draft facts and customer confirmation | Local-demo identities are simulations; draft progress comes from scripted scenes unless an external agent is integrated |

Account evidence is anchored to the existing fixed demo clock. Current case age uses the live clock. Both are labelled
in the interface; joining them into a single unqualified “today” chart would misrepresent the data.

## Implemented additions

| Addition | Officer benefit | Evidence and safeguards |
|---|---|---|
| Interactive urgency ring and issue bars | Understand the queue and open the matching cases directly | Counts come from active saved cases; the charts filter the real queue |
| Case-stage flow and open-age distribution | Find waiting, manual, completed and ageing work | Stages are mutually exclusive; age includes active work already in review |
| Decision distribution | See approved, modified and manual decisions | Counts decisions once; does not claim accuracy, recovery or satisfaction |
| Response watch | Surface urgent cases that still need their first pickup | Current P1/P2 bands, actual creation times and the README's 2/30-minute project targets; never presented as bank SLAs |
| Evidence coverage and language support | Find cases requiring verification or language assistance | Separates account signals from conversation cues; counts active cases rather than inventing confidence percentages |
| Linked outgoing payment total | Understand the size of the payments being reviewed | Deduplicates transaction IDs, checks customer ownership, excludes completed cases, and labels AUD amounts as unconfirmed outgoings rather than losses |
| Visual priority components | Explain why the backend selected a priority | Uses backend score parts; explicitly reconciles caps, floors and overrides instead of treating the subtotal as the final score |
| Customer context | Bring relevant account, payment and delivery facts into the case | Masks account references, uses only the case's customer, separates reported protection from verified state, and collapses unrelated recent history |
| Handoff brief | Give the next officer a concise, consistent starting point | Explicitly initiated copy action; no external messaging, no full account numbers or copied account balances; labels simulated data |
| Shared ownership and Mine filter | Avoid two officers acting on the same case; support a clear handoff | Server checks owner/revision, records releases and completion, and persists claims; one backend worker only |
| Live intake card | See the need and matched records as a conversation collects them | Unranked drafts stay outside queue metrics; backend-derived evidence is separated from conversation reports; explicit confirmation submits the case once |
| Live colleague updates | Notice new work, ownership changes and completed cases | Server-sent invalidations fetch fresh snapshots with backup polling; a changed case invalidates an open decision dialog |

The new visuals use local SVG, native meters and semantic controls. They require no chart service, AI API key,
production JavaScript dependency, new database, frontend build or separate server.

## Next dashboard ideas to evaluate

These are candidates, not implemented features or confirmed work in progress:

| Candidate | Existing evidence it could use | Useful validation |
|---|---|---|
| Team workload view | Current claims, active/manual stages and completion actors | Reconcile counts with saved cases; show a small prototype snapshot rather than staff productivity rankings |
| Visual handoff timeline | Pickup, release, correction, decision and completion audit events | Help the next officer find the last meaningful change without duplicating the full activity log |
| Saved filters and configurable alerts | Existing queue filters and live completion events | Check whether preferences reduce repeated clicks or alert fatigue; storing preferences would be new work |
| Further appearance refinement | Current desktop/mobile layouts, progressive disclosure and officer feedback | Test clearer hierarchy and spacing, keyboard/screen-reader flows and reduced motion before adding more visual elements |

Select the next increment from observed officer needs. Existing graphs and basic completion updates are already
implemented; the candidates above should not be reported as missing core dashboard functionality.

## Ideas to defer, and what would make them feasible

| Idea | Why it is deferred | Useful prerequisite |
|---|---|---|
| Queue forecasts and staffing recommendations | Six synthetic customers and a short saved-case history cannot support reliable demand predictions | Sustained arrival/handling history, staffing capacity, business calendars and evaluation against actual outcomes |
| Fraud network or payee risk scores | Common payees do not establish fraud; the supplied examples do not form a validated fraud network | More representative ownership-checked cases and adjudicated outcomes; keep existing cross-case signals as evidence for human review |
| “Money saved”, AI accuracy or customer happiness charts | Simulated actions and decisions contain none of these outcome measurements | Verified recovery events, labelled evaluations and consented feedback |
| Automatic translation or a new voice agent | A preferred language and one supplied translation are not a translation system | An approved translation/voice integration, credentials and a checked customer-facing workflow |
| Real callbacks, account changes or payment recovery | The repository intentionally mocks these actions | Authorised bank integrations, authentication, permissions, operational controls and end-to-end validation |
| Production identity and roles | Named Basic accounts exist, but remain prototype controls without customer identity or role separation | SSO/MFA, customer authentication, officer/protocol-owner permissions, session controls and monitoring |

## Review priorities

The browser checks exercise chart-to-case filtering, empty states, score reconciliation, customer ownership, delivery
milestones, handoff content, existing decisions, mobile layout and automated accessibility rules. Backend checks cover
deduplication, ownership boundaries, age buckets, waiting-driven priority promotion, clock separation, manual/completed
stage counts, unknown customers and inherited authentication. Reports retain checks needing manual accessibility review.

The next practical increment should be selected from observed officer feedback: which chart helps select a case,
which account fact saves a lookup, and whether handoff notes make follow-up easier. More charts should earn their place
by helping with one of those decisions.
