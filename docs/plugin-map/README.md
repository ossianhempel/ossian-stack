---
summary: The generated plugin map — one SVG board of every skill, its role, and what it runs; how map.json, the builder, and the render script fit together.
read_when:
  - Adding, removing, or renaming a skill or agent (map.json must place it, then rerun the render).
  - bun run validate fails with "plugin-map" or "map.json" in the message.
  - Changing the board's layout, colours, or lane structure.
---

# Plugin map

`map.png` at the top of the README is a screenshot of `index.html`, which draws
one SVG board from a JSON block that `scripts/build-plugin-map.js` injects.

| File | Role |
| --- | --- |
| `map.json` | Hand-curated: a role per skill, a kind per subagent, the `calls` graph, and the `sections` that say where each id is drawn. No descriptions — those come from frontmatter. |
| `scripts/build-plugin-map.js` | Walks `skills/` (and `agents/` if it ever exists), reads name, description and invocation flags from frontmatter plus origin from `sources.json`, merges with `map.json`, and rewrites the block between `<!-- plugin-map:begin -->` and `<!-- plugin-map:end -->` in `index.html`. `--check` fails instead of writing. |
| `index.html` | Self-contained page. No framework, no fetches, works from `file://`. Hover lights a node with everything it runs and everything that runs it; click opens a drawer; `?expanded=1` draws the collapsed groups. |
| `scripts/render-plugin-map.sh` | Headless Chrome screenshot at 2000px wide, once collapsed (`map.png`) and once expanded (`map-expanded.png`). |

## Roles

| Role | Meaning | Pill |
| --- | --- | --- |
| `human` | you type it (`disable-model-invocation: true`) | filled accent |
| `both` | you or another skill | outline accent |
| `auto` | only invoked by other skills | filled second hue |
| `knowledge` | reference the agent reads | dashed grey |
| subagent | dispatched by a skill | rounded purple |

## Sections

- **lanes** — one titled box per routing outcome. `steps` is the left-to-right main
  chain; `optional` marks a step, `writes` captions the artifact it produces.
  `extras` is a second row without arrows.
- **platforms** — the right-hand column, one tile per platform, skills tagged
  `setup`, `building`, or `reference`.
- **sideDoors** — utilities you run directly.
- **knowledge** — collapsed by default into `reads N` badges on the skills that
  read them; drawn as a region when expanded.

Every id must appear in exactly one section. The builder fails otherwise, and also
when a skill on disk is missing from `map.json`, when `map.json` names something
that no longer exists, or when the HTML block is stale.

## Loop

```bash
bun run map          # rebuild the JSON block
bun run map:render   # rebuild + screenshot (needs Chrome)
bun run validate     # includes build-plugin-map.js --check
```

The board's absolute coordinates live in the single `G` object near the top of the
renderer; cluster definitions (`lanes`, `platforms`, `sideDoors`, `knowledge`) live
in `map.json`. Change layout in `G`, change membership in `map.json`.
