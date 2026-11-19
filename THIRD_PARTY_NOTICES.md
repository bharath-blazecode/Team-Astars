# Attribution, assets and licensing status

## Team-authored work

SpeedQ is a Team Astars project. Members (alphabetically by given name): Agamvir Bal, Aishwarya Naidu, Amanraj Dhillon, Bharath Sampath and Karan Rooprai. **No repository-wide software licence has been agreed or added.** Public visibility is not a general reuse grant. Choosing a licence for the team's work remains an owner/team decision; this cleanup does not assign contributors' rights.

The current support-headset SVG is original project artwork, documented in [BRANDING.md](BRANDING.md). New repository screenshots show the team's running application with synthetic data. The diagrams in `assets/diagrams/` are original documentation. The workflow uses source-drawn SVG informed by the team’s whiteboard and generated layout previews; the architecture uses Graphviz. See [diagram sources and rendering](assets/diagrams/README.md). Graphviz and the headless renderer are development tools, not bundled application code.

## Vendored Retell browser bundle

`web/static/retell-web.js` is an existing vendored bundle. Its retained header attributes **retell-client-js-sdk 3.0.4, ISC licence, © Retell AI**, bundled with LiveKit. npm metadata for that SDK version also declares ISC and dependencies on `eventemitter3 ^5.0.1` and `livekit-client ^2.5.1`.

- [Retell client source](https://github.com/RetellAI/retell-client-js-sdk)
- [Version 3.0.4 package metadata](https://registry.npmjs.org/retell-client-js-sdk/3.0.4)
- [LiveKit client source and licence](https://github.com/livekit/client-sdk-js)
- [EventEmitter3 source and licence](https://github.com/primus/eventemitter3)

The existing bundle is unchanged by this cleanup. Its original build lockfile and a complete inventory of bundled dependency versions/notices are not present. The npm tarball inspected for version 3.0.4 did not contain a standalone licence file. Therefore this note records known provenance, not a claim that a full transitive licence audit is complete. Before redistributing a rebuilt bundle, record exact source versions and include the applicable upstream licence texts and notices; retain existing attribution.

Python dependencies and Node development dependencies have their own upstream terms. `backend/requirements.txt` records tested direct Python versions; it is not a full transitive lockfile. `frontend/package-lock.json` records browser-test dependencies. Neither file grants a licence to team-authored code.

## Banking references and presentation

The Westpac name identifies the hackathon context; the project is not an official bank product or an endorsement. The current application uses the original headset rather than the bank logo. The final [submitted deck](docs/submission/README.md) is preserved as a historical team artifact and may contain older artwork or claims; it is not repackaged as a new cleared asset set.

The sourced protocol summaries have separate [provenance notes](backend/data/PROTOCOLS_SOURCES.md). External hosted knowledge-base contents were not supplied or copied into this cleanup. Do not treat source citations, a public webpage or removal of a logo as blanket permission for unrelated content.
