---
summary: Upstream source map for global skills — trace vendored skills, refresh commands, and when to add entries.
read_when:
  - Vendoring or refreshing a skill from an external repo.
  - Adding a new skill to skills/ — check whether it needs a sources.json entry.
  - Asked "where did this skill come from" or "how do I update skill X".
---

# Skill upstream sources

Global skills sync as **symlinks** into agent runtimes (`~/.agents/skills`, etc.).
Editing a skill in `skills/` is instant everywhere — but **upstream repos are not
polled automatically**. Vendored skills go stale until someone refreshes them.

**Canonical map:** [`skills/sources.json`](../skills/sources.json)

## Origin types

| `origin` | Meaning |
| --- | --- |
| `local` | Authored and maintained in `ossian-stack` only. |
| `vendored` | Copied from an external repo via `npx skills add …` (or equivalent). |
| `adapted` | Started upstream; heavily customized — diff carefully on refresh. |
| `companion` | Documents an external CLI/tool; not a file-for-file copy. |
| `derived` | Encodes external docs/guidelines; manual refresh when source docs change. |

## Refresh a vendored skill

1. Open `skills/sources.json` and find the skill name.
2. Run its `refresh` command from the `ossian-stack` repo root.
3. Review the diff — skip or preserve local overrides (see `autoreview`, `CHANGELOG`).
4. Update `lastSynced` in `sources.json` and add a `CHANGELOG.md` entry.
5. Bump the plugin `version` in all three manifests, commit, and refresh the
   marketplace (see `docs/plugin-workflow.md`).

Standard pattern (also documented in per-skill `README.md` when vendored):

```bash
npx skills add <owner>/<repo> -y --skill <skill-name>
cp -R .agents/skills/<skill-name>/* skills/<skill-name>/
```

`.agents/skills/` is a local install scratch dir — never commit it.

## Adding a new skill

When creating or vendoring a skill:

1. Add/edit files under `skills/<name>/`.
2. **Add an entry to `skills/sources.json`** — every skill gets one:
   - `local` if authored here
   - full upstream + `refresh` if vendored
3. For vendored skills, add `skills/<name>/README.md` with the same refresh one-liner.
4. Drop a `CHANGELOG.md` entry and run sync.

## Listing vendored skills only

```bash
jq -r '.skills | to_entries[] | select(.value.origin == "vendored") | .key' skills/sources.json
```

## Listing by origin

```bash
# All adapted skills (manual-merge on refresh)
jq -r '.skills | to_entries[] | select(.value.origin == "adapted") | "\(.key)\t\(.value.repo // "n/a")"' skills/sources.json

# All local-only skills
jq -r '.skills | to_entries[] | select(.value.origin == "local") | .key' skills/sources.json
```

**Origin breakdown (2026-07-27):** 22 vendored · 9 adapted · 7 companion · 2 derived · 13 local (53 total).

## Related

- [`docs/syncing.md`](syncing.md) — how symlinks install to runtimes
- [`docs/update-changelog.md`](update-changelog.md) — when to log skill changes
