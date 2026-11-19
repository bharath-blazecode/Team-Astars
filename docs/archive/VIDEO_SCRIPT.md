> **Historical rehearsal material.** This outline predates the final 14-slide submission.
> The video was submitted on 17 November 2026. See the [submission record](../submission/README.md).
> Checkboxes here are preserved notes, not outstanding hackathon tasks.

# Westpac SpeedQ: presentation script

Team Astars · QUT · working target **about 7:15**: about 4:45 of slides/transitions plus a 2:30 walkthrough.
Confirm the official duration and submission rules; this is the team's timing plan, not a verified competition limit.

The script follows the deck as it stands now, in slide order:
[Westpac SpeedQ Pitch](https://claude.ai/artifact/3HyTVvX6TuDo6jw6gof3C3)

The selected video format is narrated presentation slides. Use prototype screenshots for the walkthrough; a screen
clip is optional. This edit preserves the team's slide order and speaker split, but does not update the external
deck. Reconcile the deck with this script before export, especially slides 4 and 13. The narration below uses no
unverified external statistics.

**Demo boundaries:** all customer data is synthetic; login and banking actions are simulated. The default
walkthrough uses `/demo`: Sam's P4 response requires officer approval. If the team instead captures a fully answered
live Clario Tier 1 question, Sam can remain outside the queue; use narration matching that captured flow. Check
[current headset mark](../../BRANDING.md#logo-use-in-the-dashboard-and-presentation) and the
[recording checklist](VIDEO_SHOT_LIST.md) before submission.

**Speakers:** the split below is a suggestion so all five of you appear. Swap freely.

| Speaker | Slides |
|---|---|
| **Amanraj** | 1–3 (open and problem) |
| **Bharath** | 4–7 (evidence, insight, product, pipeline) |
| **Aishwarya** | 8–9 (card and queue) |
| **Karan** | 10 + demo |
| **Agamvir** | 11–15 (trust, outcome, why now, roadmap, close) |

**Delivery cues:** `[beat]` = a one-second pause · `[click]` = next slide · **bold** = lean on the word.
At about 150 words a minute, each section below fits its time if you don't rush the beats.

---

## Act 1: the problem

### Slide 1 · Westpac SpeedQ · ~12 s · Amanraj
> Right now, someone’s life savings are leaving their bank account…
> `[beat]`
> …and they’re listening to **hold music**.
> We’re Team Astars from QUT, and this is **Westpac SpeedQ**, our independent hackathon prototype using synthetic data. `[click]`

### Slide 2 · Two calls. One line. · ~25 s · Amanraj
> Meet Maria, 64. A very convincing man “from the bank” just told her to move her savings. So she did: **$4,800**, to a stranger.
> And meet Sam, 27. He’s eating cereal, wondering when his new card arrives.
> In this illustrative story, they join the **same line**, even though their needs are very different. `[click]`

On-screen label: **Illustrative scenario, not measured bank waiting times.**

### Slide 3 · Officers start every call from zero · ~18 s · Amanraj
> And on the other end?
> “Customer number?” `[beat]` “What happened?” `[beat]` “Let me transfer you…”
> Every call starts from **zero**. No context, no idea who’s in danger, and the next call is already waiting. `[click]`

---

## Act 2: the product

### Slide 4 · Why context and urgency matter · ~18 s · Bharath
> Our prototype addresses two problems: customers repeating the same story, and officers starting without a clear view of urgency.
> The goal is straightforward: carry the context forward and make priority **explainable**. `[click]`

Update the matching deck slide. Add external statistics only after checking and citing their primary sources.

### Slide 5 · The officer doesn’t know the severity of the problem · ~8 s · Bharath
> *(Slow down. Let the red slide land.)*
> The problem isn’t slow officers. `[beat]` It’s that **the officer doesn’t know the severity of the problem.** `[beat]` `[click]`

### Slide 6 · Meet Westpac SpeedQ · ~20 s · Bharath
> So we built two parts that work together.
> **Clario** is the conversational front door in our customer-app prototype: it gathers the need, offers simulated protection first, and writes the problem up **once**.
> **Prorio** is deterministic code: it ranks cases from harm and account evidence, and drafts a protocol proposal.
> And a **human** still makes every decision. `[click]`

### Slide 7 · One journey, start to finish · ~28 s · Bharath
> Here’s the whole journey.
> Tap **Get help**. In this prototype, the demo customer is already selected; production identity remains future work.
> Clario gathers the need and, for a scam, offers the simulated **protect-first** flow.
> It writes **one card** you can see and correct.
> Prorio scores the harm and drafts the protocol.
> The officer decides: **Approve, Modify or Manual**.
> You get status updates; scripted scenes include supplied translations, while live language behaviour needs rehearsal.
> Officer feedback can suggest a protocol improvement, with a **human signing off** before it changes. `[click]`

### Slide 8 · Explain it once · ~20 s · Aishwarya
> Clario has four doors. Your account? Answered from **your data**. A general question? Answered **with a source**. A scam? **Protect first.** Want a person? Clario **never** says no.
> And the officer gets this: Maria’s card, which she can see and fix herself.
> One story. Told **once**. `[click]`

### Slide 9 · Most at risk, first in line · ~22 s · Aishwarya
> Who goes first? Three questions: **How much could they lose? How soon? Does the account data back it up?**
> So Maria’s scam goes to the top. Jordan, locked out and unable to buy groceries, next. Then Priya’s mystery charge.
> And Sam's delivery question is lower priority, ready for a quick approved response.
> And it’s ranked by **code, not AI**, so just typing “scam” **won’t** get you to the front. `[click]`

### Slide 10 · Let’s see it · ~3 s + demo ~2:30 · Karan
> **Let’s walk through it.** `[advance through the prototype screenshots]`

#### Walkthrough narration (over presentation screenshots, or an optional screen clip)

**1 · Sam asks about his card (~20 s)**
> Sam asks when his card’s coming. The proposed answer uses **his own data**: the 19th. In this scripted P4 flow, the officer approves the response and Sam sees the outcome.

**2 · Maria reports the payment (~25 s)**
> Now Maria. She sent money to a new payee because “the bank” told her to. Before any queue, Clario offers the simulated **SafeBlock** step. **Protect first** is the design; no real account is changed here.

**3 · The card builds live (~20 s)**
> These screenshots show her card taking shape in **Live intake**. She confirms it, and the backend ranks it.

**4 · Ranked P1 (~25 s)**
> In this captured example: **P1, score 100**. The explanation shows the harm, urgency and account evidence. The score is calculated by code, with the reasons visible.

**5 · The officer approves (~25 s)**
> The officer claims it. The story, evidence and drafted protocol are together. The officer reviews the checks, chooses **Approve**, and confirms the decision. A second officer can see ownership and completion.

**6 · Maria sees the outcome (~15 s)**
> Maria’s status updates live, with a reference number.

**7 · The learning loop (~20 s)**
> When officers change a plan, SpeedQ can suggest a protocol update for human approval. This is a reviewed rule change, not automatic model retraining.

> `[return to the closing slides]`

---

## Act 3: the outcome

### Slide 11 · AI can close doors. Only people open them. · ~20 s · Agamvir
> “AI in a bank” raises one question: **what if it gets it wrong?**
> Our rule: **AI can close doors. Only people open them.**
> Code does the ranking. The AI **never moves money**. AI drafts, a human decides, and **everything is logged**. `[click]`

### Slide 12 · Same two calls. Different outcome. · ~20 s · Agamvir
> Let’s replay those calls.
> Maria goes through the simulated protection step first, her urgent case ranks at the top, and the officer already has her story.
> Sam gets the card-delivery answer after the approved P4 plan.
> And the officer? One card. **One decision.** `[click]`

### Slide 13 · Built for where Westpac is heading · ~18 s · Agamvir
> SpeedQ combines customer context, explainable priority and human approval in one prototype journey.
> The next question is whether it helps real officers choose and finish the right case. That needs a user-tested pilot. `[click]`

Update the matching deck slide; claims about bank deployments, regulations or measured outcomes need checked sources.

### Slide 14 · Working today. Ready to grow. · ~12 s · Agamvir
> The core dashboard, collaboration and live Retell integration are **implemented**, with automated tests.
> Next: complete the live rehearsal and usability review. Surge mode, production identity and real banking integrations remain future work. `[click]`

### Slide 15 · Right person. Right order. Right time. · ~10 s · Agamvir (or all five on camera)
> Because when your money’s on the line… you shouldn’t have to **wait in line**.
> `[beat]`
> **Westpac SpeedQ.** Right person. Right order. Right time. Thank you.
> `[hold the slide in silence for two seconds, then end]`

---

## Recording tips

- **Energy.** Smile, sit up, and speak a little faster and louder than feels natural. Recordings flatten energy.
- **Lines to land.** The pause after “hold music”, “Sorry, Sam”, and the final tagline.
- **Pace.** Read your part aloud once with a timer. If you run long, cut words, not the pauses.
- **Takes.** Record each speaker’s section as a separate take, so one mistake doesn’t mean redoing everything.
- **Walkthrough.** Capture the prototype states first, place them in the slides, then narrate them in order. Use a screen clip only if the team chooses one.
- **Honesty.** Keep the illustrative-scenario label on slide 2, identify scripted captures and simulated actions, and use only checked external facts.
- **Export.** Follow [SHOT_LIST.md](VIDEO_SHOT_LIST.md), retain a PDF deck backup and review the complete video before submission.
