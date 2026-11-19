# Diagrams and editable sources

## Customer-support workflow

- [pipeline.svg](pipeline.svg) is the canonical editable artwork, including title/description text for accessibility. It replaces the earlier six-box draft.
- [pipeline.png](pipeline.png) is rendered directly from that SVG for slide/portfolio use.
- [Workflow explanation](../../docs/workflow.md) maps the whiteboard's four routes to the actual implementation and hosted-service boundaries.

The final artwork is source-drawn SVG. The owner's whiteboard and historical notes supplied the routing; generated layout previews informed the visual direction. Connections were checked against the code, including confirmation before ranking and officer review before recorded outcomes. The source has no scripts, external fonts, embedded photos or external resources.

To regenerate the PNG after editing the SVG, install the frontend development dependencies from [BUILD.md](../../BUILD.md#validation), then run from the root:

```bash
node tools/render-diagrams.cjs
```

This uses a headless browser to render the SVG. `BEACON_CHROMIUM` optionally selects a Chromium executable.

## Component architecture

[architecture.dot](architecture.dot) is the Graphviz source for [architecture.svg](architecture.svg) and [architecture.png](architecture.png). It shows repository components, persistent state and the external Retell boundary, rather than repeating the customer journey.

```bash
dot -Tsvg assets/diagrams/architecture.dot -o assets/diagrams/architecture.svg
dot -Tpng assets/diagrams/architecture.dot -o assets/diagrams/architecture.png
```

All diagrams describe a synthetic-data hackathon prototype with simulated banking actions. The workflow's feedback loop requires human approval of a protocol version.
