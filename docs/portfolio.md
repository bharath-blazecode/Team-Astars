# Portfolio and résumé material

## Team project summary

**SpeedQ — explainable customer-support triage**
Completed in a five-person team for the Westpac Innovation & Coding Competition 2026; submitted 17 November 2026.

SpeedQ explores how a confirmed customer-service card, evidence-based priority rules and an officer review workspace can reduce repeated context-building and make urgent needs visible. The implementation combines a Python/FastAPI backend, SQLite, plain JavaScript interfaces and optional hosted Retell voice/chat integration. The demonstration uses synthetic records and simulated banking actions.

[Watch the submitted video](https://youtu.be/2Sc_2JRPxVs) · [View the final deck](submission/Westpac-SpeedQ-Pitch-submitted.pptx) · [Dashboard](../assets/screenshots/dashboard-desktop.png) · [Pipeline](../assets/diagrams/pipeline.svg)

## Safe starting résumé wording

> Worked in a five-person team to deliver SpeedQ, a customer-support triage prototype using Python/FastAPI, SQLite and JavaScript, with customer-confirmed case intake, explainable prioritisation and an officer review dashboard.

This is team-level wording. Before publishing a stronger personal bullet, confirm which components you personally designed, implemented, integrated, tested or presented. Commit counts alone do not establish ownership. Do not copy a placeholder claim into a résumé.

The [whiteboard-to-prototype walkthrough](workflow.md) explains the original four-route idea and the implementation decisions behind the final diagram.

## Evidence worth discussing

- Why structured deterministic scoring was kept separate from conversational intake.
- How drafts, customer correction and explicit confirmation precede queue admission.
- How claims and revisions coordinate two officers without silently overwriting decisions.
- Why protocol changes require human approval.
- What the tests establish, and where external live services and production needs remain outside that evidence.

The cleanup validation passed seven backend suites and 103 browser checks on Linux. Those counts are verification facts, not measured customer impact. Native Windows CI results must be checked separately.

## Team credits

Team Astars members, listed alphabetically by given name:

- Agamvir Bal
- Aishwarya Naidu
- Amanraj Dhillon
- Bharath Sampath
- Karan Rooprai

## Remaining evidence gaps

Personal contribution details and a factual summary of the submitted demo's live voice/chat/transfer behaviour have not yet been supplied. A sanitised hosted-agent configuration could improve live reproduction documentation. The offline scripted demonstration is available without it.

The team completed and submitted the hackathon prototype and presentation-slide video on 17 November 2026.
