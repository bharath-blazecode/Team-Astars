# Westpac SpeedQ branding

**Merged and verified:** [PR #14](https://github.com/bharath-blazecode/Team-Astars/pull/14) merged commit `d057af0`
into `main` at `60adbde`. Git remote ancestry and matching file trees were checked on 17 Nov 2026 (Brisbane).

The team renamed Beacon Assist to **Westpac SpeedQ** and chose to retain the original dashboard partitions, sidebar
and case workflow. The later horizontal-navigation concept was not selected. This update changes the name, mark and
colour system across the current dashboard, API reference and retained demo pages.

## Palette and interaction

| Role | Colour | Use |
|---|---|---|
| Brand/action | `#DA1710` | Primary buttons, current selections, active chart accents |
| Action hover | `#B5120C` | Hover and high-emphasis red text |
| Navigation | `#54100E` | Existing sidebar, retaining the selected layout |
| Navigation selection | `#85231B` | Current sidebar item |
| Panel | `#FFFFFF` | Existing work panels |
| Canvas | `#F7F7F6` | Quiet off-white background |
| Primary text | `#252525` | Headings and case information |
| Secondary text | `#535353` / `#636363` | Labels and supporting detail |

Colours are centrally defined in `frontend/styles.css` and used by insights and live intake. Functional priority,
warning and verified-state colours remain distinct and text-labelled. Primary buttons have red hover/pressed states;
keyboard focus is red on light surfaces and white within the dark sidebar. Layout and decision semantics are retained.

## Westpac mark provenance

`frontend/westpac-mark.svg` contains the three static paths from the published `WBCLogo` component in
[`@westpac/ui` version 1.21.0](https://www.npmjs.com/package/@westpac/ui/v/1.21.0), distributed by Westpac GEL.
The reviewed source is
[wbc-logo.js](https://cdn.jsdelivr.net/npm/@westpac/ui@1.21.0/dist/components/symbol/components/logos/wbc-logo.js),
with copyright metadata supplied by
[symbol.component.js](https://cdn.jsdelivr.net/npm/@westpac/ui@1.21.0/dist/components/symbol/symbol.component.js).
The published paths, proportions, `#DA1710` fill and “Copyright © 2025 by Westpac Banking Corporation. All rights
reserved.” notice are retained. A local white surround keeps the red mark readable in the existing dark sidebar.

The published package metadata declares MIT for the UI package; that does not establish permission to represent
Westpac or confer rights to its trademarks. The mark is included at the team's explicit request for this independent
hackathon demonstration. The dashboard continues to identify Team Astars and states that it is not an official
Westpac service. Competition brand-use and content guidance still apply.

## Scope of source review

The source was read as text; its React code was not installed or executed. The saved asset contains only SVG,
metadata and path elements, without scripts, event handlers, embedded HTML, external references or remote resources.
It is served from the existing same-origin asset allowlist under the current browser security policy.

Direct access to the Westpac live website is blocked by the current cloud network policy, and no authenticated
Westpac app was available. The reference is the published GEL component and its actual mark colour; this is not a
claim to have reviewed a current private bank app or internal officer dashboard. No additional dashboard packages,
external fonts or runtime dependencies were introduced.
