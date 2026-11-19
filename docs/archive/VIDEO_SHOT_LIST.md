> **Historical rehearsal material.** This outline predates the final 14-slide submission.
> The video was submitted on 17 November 2026. See the [submission record](../submission/README.md).
> Checkboxes here are preserved notes, not outstanding hackathon tasks.

# Westpac SpeedQ: presentation-slide video plan

Team Astars is making the submission video from **presentation slides with recorded narration**. Use original
slide diagrams and screenshots captured from this prototype. The deck and exported video are still to be produced;
this document is the production plan.

The team's existing **15-slide order and speaker allocation** are recorded in [SCRIPT.md](VIDEO_SCRIPT.md). Keep that
structure rather than introducing another deck concept. The working target is **about 7:15**, including a roughly
2:30 walkthrough, in 16:9. Confirm the actual competition duration, format, deadline and upload rules; the team's
timing target is not a verified competition limit.

## Slide sequence

| Slides | What to show | Narration and evidence |
|---|---|---|
| 1. Westpac SpeedQ | Team Astars, the project name and the opening line | Introduce the independent prototype and synthetic data; apply [brand-use guidance](../../BRANDING.md). |
| 2–3. The customer and officer problem | Maria/Sam journey and the loss of context across handoffs | Label the story illustrative; show no invented bank wait-time measurements. |
| 4–5. Context and urgency | The problem statement and the need to understand severity | Use sourced evidence only where the actual source is verified; the script supplies narration without unsupported statistics. |
| 6–7. Product and pipeline | Customer → Clario → confirmed card → Prorio → officer → outcome | Distinguish the conversational agent from deterministic ranking code. Prototype login and banking protection are simulated. |
| 8–9. The card and priority queue | Read-back/correction and priority with reasons | Use screenshots of the actual run. Scores are project priority, not AI confidence or predicted loss. |
| 10. Walkthrough | Presentation screenshots revealing draft → confirmation → ranking → review → outcome | Follow the walkthrough in [SCRIPT.md](VIDEO_SCRIPT.md). A short screen clip is optional; still screenshots support a slide-only recording. Label scripted scenes. |
| 11–12. Human control and outcome | Approval/checks, audit trail and customer status | Show the actual approval confirmation and shared ownership. The scripted Sam P4 flow needs approval; a fully answered live Clario Tier 1 question can stay outside the queue. |
| 13–14. Relevance and delivery | Benefits supported by the prototype, implemented work and remaining validation | Live Retell integration is built; live rehearsal remains pending. Keep future surge mode and production identity separate. |
| 15. Close | Existing team closing message and credits | Keep the selected tagline and team attribution; finish with an honest prototype claim. |

The actual deck is externally maintained. Reconcile its text with the script before recording, especially slides
4 and 13 if they still contain unverified external statistics. Keep one main message per slide and put a checked
source beside every external factual claim. Read the narration aloud to set the final timing.

## Build the slides

1. Use the team's preferred slide editor. Choose large readable type, white/off-white backgrounds and restrained
   red accents matching the dashboard. Keep the current dashboard layout in screenshots.
2. Use diagrams, short labels and speaker notes. Crop screenshots to the relevant interaction rather than shrinking
   an entire dashboard into an unreadable slide. Use simple reveals to explain the handoff in order.
3. Record your own narration in a quiet room. Add captions or provide the narration transcript. Use readable contrast
   and avoid rapid transitions or information conveyed only by colour.
4. Include Team Astars, the synthetic-data disclosure and independent-prototype statement. Use the original support
   headset with one microphone; replace older bank marks and screenshots in the deck. See [BRANDING.md](../../BRANDING.md).
5. Keep researched claims separate from the example story. An illustration of a slow queue is not a measurement of
   Westpac's actual service. Use verified sources for external statistics, or leave those statistics out.

## Capture the prototype

Follow [BUILD.md](../../BUILD.md) for the current setup and [the README recording guide](README.md#recording-the-video).
Use a disposable rehearsal database before using **Reset demo**; preserve existing team cases.

- Officer workspace: `/officer` (or `/`). Use **Load sample cases** for an additive synthetic queue.
- `/demo` shows the full-width officer workspace. Capture customer screens separately at `/customer`, or open
  **Live intake → View customer conversation** for the optional preview. Capture only the states needed for the slides.
- Show draft → confirmation → ranking → officer review → outcome in order. Capture the reasons shown by the backend.
- For collaboration, use two local demo officer tabs and show an actual claim or named completion.
- For a learning-loop screenshot, a disposable demo can use `NRY_SUGGEST_THRESHOLD=1`. Restart after changing settings.
- Live voice/chat requires the configured Retell agents and [LIVE_TEST_CHECKLIST.md](../../LIVE_TEST_CHECKLIST.md).
  The deterministic scripted fallback remains available without an external AI key.

## Claims and assets

- SafeBlock, card locks, disputes, callbacks and payment recall are simulated or drafts. No money is moved.
- A screenshot of a live intake card does not establish that a real phone transfer worked. The configured fictional
  transfer number cannot connect to a real fraud team.
- Demo timing is illustrative. Do not claim measured wait reduction, fraud accuracy, recovery totals or satisfaction.
- Source/copyright guidance is in [PROTOCOLS_SOURCES.md](../../backend/data/PROTOCOLS_SOURCES.md). Capture this prototype's
  interface rather than importing Westpac website photographs or marketing artwork.

## Record and export

- [ ] Confirm the competition's duration, deadline and file/link requirements; use the original headset mark and current screenshots.
- [ ] Reconcile the existing 15-slide deck with [SCRIPT.md](VIDEO_SCRIPT.md), keeping its team speaker allocation and confirming a final reviewer.
- [ ] Capture current screenshots, label scripted scenes and check that only synthetic data is visible.
- [ ] Finish the slide deck and speaker notes. Check text at normal presentation size.
- [ ] Record the slide presentation with narration using the chosen editor or screen recorder.
- [ ] Export a broadly playable video, such as MP4 at 1080p if the submission rules permit it; retain a PDF deck backup.
- [ ] Watch the complete export on another device, checking sound, captions, cropping, pacing and readability.
- [ ] Verify the submission link/file opens with the intended access, then submit through the official process.

## Current delivery status

The software is implemented on `main` through PR #21. This revision replaces the bank mark with the original
headset. The refreshed slide captures, narration, final export and live Retell rehearsal are **not marked complete**
by this document. Update this checklist only when
the team has the corresponding evidence.
