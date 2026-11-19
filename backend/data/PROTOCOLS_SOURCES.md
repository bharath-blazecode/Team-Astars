# Protocol Database: where it comes from, and how we stay on the right side of copyright

`protocols.json` is the Westpac SpeedQ Protocol Database: 31 scenarios Prorio can use to draft proposals. This note
explains how it was built and the rules for changing it.

## What it is and isn't

- It is **our own summary**, in our own words, of how banking situations are handled, based on **public** pages read
  on 16 Nov 2026: Westpac's help, security and FAQ pages, plus Australian rules and guidance (ASIC's ePayments Code,
  AFCA, ASIC RG 271 via AFCA, Moneysmart, the Australian Banking Association, Legal Aid NSW).
- It is **not** Westpac's internal procedure, and it does not claim to be. Steps marked `team_design` are our own
  design choices, not published rules.
- Every protocol lists its sources (titles and links). Facts can change; check the link before relying on one.

## The copyright position (read before adding anything)

The team's source review on 16 Nov 2026 recorded restrictions on reproducing or redistributing Westpac website
content ([website terms](https://www.westpac.com.au/terms-and-conditions/)). The current review could not reopen those
terms because the cloud network blocks that host. Verify the current terms and applicable competition permission;
this document records provenance and editorial safeguards, not legal clearance. Crawler access does not itself
authorise reuse.

So the database follows these rules:

1. **Summarise in our own words.** Keep facts distinct from source wording and check that each proposed reuse is
   within the applicable terms or permission. Paraphrasing alone is not a permission check.
2. **Avoid copied passages.** The earlier 16 Nov 2026 review reported no matching run of eight or more words across
   44 Westpac pages. That was an editorial overlap check, not a legal threshold or licence; it was not rerun here.
3. **Cite sources.** Each source has a title and link so readers can check the current guidance.
4. **No page dumps in the repo.** Don't commit crawled pages, screenshots of Westpac pages or PDFs. The team's
   current dashboard uses an original customer-service headset with its source documented in
   [BRANDING.md](../../BRANDING.md). The former bank logo is removed; this does not authorise copying site assets or content.
5. **No phone numbers or email addresses** from Westpac pages; they go out of date. Point to the source page instead.
6. **Not an endorsement.** Don't present this as Westpac-approved. It is a hackathon prototype using synthetic data.

Two follow-ups remain open:

- **Record the applicable permission.** Ask the competition organisers or Westpac's authorised permission owner
  about public help summaries, the retained project name and the historical slide presentation. The current dashboard uses original headset artwork. Mentor feedback is useful;
  record the rule or authorisation and its scope rather than treating informal approval as blanket permission.
- **Check the external Retell knowledge base.** Earlier team notes report 406 crawled Westpac pages in a third-party
  service; its current contents and permission were not inspected in this repository review. Confirm authorised
  reuse with its owner, or replace unsupported material with content the team is permitted to use.

## The Westpac design system (for the UI)

Earlier palette research consulted Westpac GEL. The current dashboard does not install that UI package or bundle
the bank logo. Its original headset symbol is documented in [BRANDING.md](../../BRANDING.md), separately from the
public-help source material. Project naming and any other external content still follow the applicable competition
guidance; keep the independent Team Astars attribution and avoid implying bank approval.

## How the database is meant to change ("officers teach, leads approve")

- Officers **suggest** changes through Modify or Manual decisions; nothing edits this file directly from the dashboard.
- A protocol owner approves a change; the protocol's `version` goes up (2.0 to 2.1) and the change is added to its
  history (the `change_log` field).
- Any new fact must come with a source link, in our own words, or be marked `team_design`.

## What each protocol contains

`issue_type`, `title`, `version`, `harm_category` (the technical-reference harm row it scores under), `min_band` (a gate, if any),
`clario_can_answer` (what Clario may tell the customer straight away), `protect_first` (the protective action offered
before queuing, always the customer's choice), `steps` (who does what, each with a source), `ai_may`, `officer_must`,
`required_checks`, `customer_message` (template), `timeframes` (each with a source), `notes`, `sources`.

Issue types mapped to the technical-reference harm table: SCAM_ALREADY_PAID, VERIFY_CONTACT, UNAUTHORISED_ONLINE_BANKING,
IDENTITY_THEFT, LOGIN_HELP, ACCOUNT_RESTRICTED_ID_CHECK, PAYMENT_LIMIT_CHANGE, CARD_DECLINED, CARD_ACTIVATION,
PENDING_TRANSACTION, DIRECT_DEBIT_STOP, BPAY_MISTAKE, PAYID_ISSUE, FAMILY_VIOLENCE_FINANCIAL_ABUSE,
TRUSTED_PERSON_ACCESS, ELDER_FINANCIAL_ABUSE, BEREAVEMENT, GAMBLING_HARM, ACCOUNT_CLOSURE, OUTAGE_INCIDENT. Each maps
to an existing harm category (`_about.harm_categories` holds the points), so the scoring model doesn't change. The
README lists every issue type with its category and gate.

Gates set in the data: G3 (officer-only, never below P3) for detail changes, limit changes, identity and access cases,
and giving a trusted person authority; G7 (safety cases never below P2) for family violence, financial abuse and elder
financial abuse.
