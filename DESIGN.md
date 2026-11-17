# Westpac SpeedQ officer workspace

The officer's first question is “who needs help next?” The first screen answers that with an evidence-ranked queue,
four live counts and a short preview of one customer. The interface never invents response-time statistics or case data.

**Current state:** the core dashboard, visual insights and shared ownership/live intake are implemented on `main`.
The Westpac SpeedQ red branding is merged through PR #14, verified at `60adbde` on 17 Nov 2026 (Brisbane).
The appearance and feature set remain open to further iteration;
see the [remaining work in README](README.md#remaining-work-and-next-iterations). This document describes current
behavior rather than declaring the design final.

## Information flow

1. **Scan:** priority, customer, issue, waiting time and status. Search names, references and issue descriptions, or
   filter by priority and waiting status. The scoring engine remains deterministic and unchanged.
2. **Preview:** a short need statement, the primary priority reason and up to three recommended actions. Selection is
   read-only; it does not notify the customer that an officer is working on the case.
3. **Review:** explicitly pick up the case. The case workspace separates the customer's need, recommended plan and
   customer-visible progress. Evidence, sources, protocol conditions and activity history are available on demand.
4. **Decide:** approve, modify or handle manually. A confirmation dialog shows actions and checks before a decision
   is sent. Double submission is blocked while the request is running. Backend conflict checks remain authoritative.
5. **Finish:** automatic/mock decisions record outcomes immediately. Manual cases stay in **In review** until the
   officer writes the customer outcome. Completed cases and their audit trails remain accessible.
6. **Improve:** modifications and manual handling feed the existing learning loop. Suggestions remain separate from
   active protocols until the configured threshold is reached and a human approves a new version.

Required-check acknowledgements are interface safeguards, not proof that a real-world banking check occurred. The
prototype still simulates every banking action. Incomplete customer-message drafts require manual handling in this UI.

## Visual direction and branding

The team retained the original sidebar, panel partitions, queue/preview and focused case review. The alternative
horizontal-navigation concept was not selected. The project is now **Westpac SpeedQ**.

The colour system uses Westpac's published `#DA1710` red for primary actions, `#54100E` deep red for the sidebar,
white panels, off-white `#F7F7F6` canvas and neutral charcoal/grey text. Purple decorative surfaces and secondary text
have been replaced across the queue, insights and live intake. Customer avatars are neutral; priority and verification
colours still convey meaning alongside text. Existing spacing, typography and information partitions are retained.

The requested minimalist direction is interpreted as restrained accents, consistent controls, neutral work surfaces
and clear hierarchy. It is a visual preference, not a gendered design rule. Buttons have distinct hover, pressed and
keyboard-focus states; the sidebar uses a contrasting white focus outline.

The Westpac mark was sourced from the published GEL `WBCLogo` component, kept locally as static SVG with its
copyright metadata, and added at the team's request. [BRANDING.md](BRANDING.md) records its provenance and usage
boundaries. This is not a reproduction of a Westpac site or private staff app. No proprietary fonts, trackers,
remote runtime assets or UI packages are loaded. The interface retains Team Astars, synthetic-data and independent
hackathon prototype disclosures.

These choices reduce copying and affiliation risks; they do not constitute legal clearance. Follow the competition's
brand-use rules and obtain permission before representing the prototype as an official bank service.

## Accessibility and resilience

- Semantic headings, labels, table headers, a skip link, visible keyboard focus and native modal dialogs.
- Search shortcut `/`, Escape to dismiss dialogs/navigation, and required fields before recording decisions.
- Mobile navigation hides its contents from keyboard focus while closed and blocks background clicks while open.
- Responsive queue and case layouts; reduced-motion preferences are respected.
- Connection errors are explicit; stale counts remain visible with an updates-paused status. A failed write stays
  in its dialog with an error instead of showing a false success. Background tabs pause polling.

## Security boundaries

The new interface is served by FastAPI on the same origin as its APIs, avoiding a separate frontend server and CORS
exceptions. All API-derived text is inserted as text nodes; source links must use HTTPS and cannot embed credentials.
There are no inline scripts or event handlers. A strict CSP limits scripts, styles and connections to the same origin;
framing, MIME sniffing, unnecessary browser permissions and caching are restricted. API documentation is self-hosted.

The default synthetic-data demo binds to loopback and rejects remote staff clients. Setting `NRY_STAFF_PASSWORD`
or the distinct-account mapping `NRY_STAFF_ACCOUNTS` enables Basic authentication for all staff pages and APIs,
including administrative operations. Authenticated audit actors come from the server identity, not a caller's chosen
name. Use HTTPS and a strong secret for remote access.
The voice webhook and secret-based case intake use `NRY_WEBHOOK_SECRET`; remote intake and protected staff mode
refuse intake when that secret is missing. Host validation and same-origin checks reject unsolicited browser writes.

Before a production pilot, replace prototype Basic accounts with organisation SSO, distinct officer/protocol-owner
permissions, session lifecycle controls and operational monitoring. SQLite and process-local state still target a
single-process demonstration. This change does not connect to real banking systems or turn simulated actions into
real operations.

## Validation

The [README test commands](README.md#tests) cover Prorio, the API, restart persistence, dashboard access controls,
insights and multi-officer collaboration. `npm test` runs both browser suites, including the actual customer demo.
Browser tests use isolated databases/processes, preserve the developer's data and capture desktop/mobile screenshots.
Manual officer usability and keyboard/screen-reader review remain on the roadmap; automated checks are not a complete
accessibility assessment. The interface has no build step or production Node dependency.

## Visual insights and case context

Care insights is a separate workspace so that extra information does not crowd the primary queue. Its charts have
text labels and counts, support keyboard input, and link directly to matching cases. Totals describe the saved local
workspace rather than a fabricated daily trend. Current priority drives the response watch, including cases promoted
by waiting; its targets are project design choices. Linked outgoing amounts are deduplicated and checked against the
case's customer and do not represent confirmed loss or recovery.

The Evidence tab shows the backend's five score components and the net effect of caps, floors or an officer override.
It never interprets a score as model confidence. The Customer context tab uses only the current case's customer and
keeps account-record protection separate from customer-reported actions. Recent unlinked history is collapsed. A
replacement card's expected date remains an expectation, not a completed delivery. A handoff brief can be copied only
through an explicit staff action and contains no account balances or full account numbers.

The same origin, strict CSP and text-node rendering apply to the new SVG charts, context and handoff text. There are
no external chart libraries or analytics trackers. New data endpoints require the same access controls as the queue.
See `FEATURE_REVIEW.md` for the source inventory, implemented choices and prerequisites for future ideas.

## Shared ownership and live intake

The queue is a team view. A server-enforced claim identifies the responsible officer, **Mine** filters active assigned
work, and release leaves an audit note before another officer claims it. A case revision accompanies website decisions;
updates invalidate open approval dialogs rather than silently replacing their contents. Other officers see read-only
case controls, named completion and updated counts through a same-origin event stream, with backup refresh on failure.

Unconfirmed cards live in a separate draft store and **Live intake** view. Facts arrive from the customer demo at the
point they are collected, with backend-derived signals kept separate from caller reports. No score or executable plan
appears until confirmation. The intake handoff then follows the real queued, assigned and completed case. The scripted
customer demo is labelled; this does not claim a new live language-model or Retell progress integration.

Local demo identities are per-tab simulations. Configured Basic accounts have distinct server-derived identities;
neither body-supplied names nor demo headers override them. Claims and draft revisions survive a restart. The deployment
remains single-worker until database coordination and event transport are shared across processes. See
`COLLABORATION_PLAN.md` for the walkthrough and delivery scope.
