---
summary: Upstream source map for global skills — trace vendored skills, refresh commands, and when to add entries.
read_when:
  - Vendoring or refreshing a skill from an external repo.
  - Checking whether vendored skills have gone stale.
  - Adding a new skill to skills/ — check whether it needs a sources.json entry.
  - Asked "where did this skill come from" or "how do I update skill X".
---

# Skill upstream sources

The plugin ships `skills/` as-is — the runtime copies the tree into its own cache.
Nothing polls upstream, so vendored skills go stale silently until someone refreshes
them. `skills/sources.json` records where each one came from and which upstream
commit the local copy is pinned to.

**Canonical map:** [`skills/sources.json`](../skills/sources.json)

## Origin types

| `origin` | Meaning |
| --- | --- |
| `local` | Authored and maintained in `ossian-stack` only. |
| `vendored` | Copied from an external repo via `npx skills add …` (or equivalent). |
| `adapted` | Started upstream; heavily customized — diff carefully on refresh. |
| `companion` | Documents an external CLI/tool; not a file-for-file copy. |
| `derived` | Encodes external docs/guidelines; manual refresh when source docs change. |

## Entry fields

| Field | Meaning |
| --- | --- |
| `origin` | See the table above. |
| `repo` | Upstream repo URL. |
| `path` / `upstreamPath` | Path within the upstream repo. `upstreamPath` is the resolved, API-verified one the drift checker queries; `null` means repo-wide. |
| `upstreamRev` | Upstream commit our copy is pinned to. The drift check compares against this. |
| `upstreamCheckedAt` | When `upstreamRev` was last confirmed. |
| `lastSynced` | When files were actually copied down. |
| `refresh` | One-liner that re-vendors the skill. |

## Check for drift

```bash
scripts/check-upstream.sh            # only skills whose upstream moved
scripts/check-upstream.sh --all      # include up-to-date ones
```

Repo-local dev tool — not shipped in the plugin. Needs `gh` (authenticated) and `jq`.
Exits non-zero when anything drifted, so it works in a pre-release check. Each drifted
skill prints a GitHub compare URL and its `refresh` command; `adapted` skills are
flagged as merge-by-hand.

After refreshing a skill, pin the new rev:

```bash
scripts/check-upstream.sh --record <skill-name>
```

That sets `upstreamRev`, `upstreamCheckedAt`, and `lastSynced` in one go.

## Refresh a vendored skill

1. Open `skills/sources.json` and find the skill name.
2. Run its `refresh` command from the `ossian-stack` repo root.
3. Review the diff — skip or preserve local overrides.
4. Run `scripts/check-upstream.sh --record <name>` to pin the new rev.
5. Bump the plugin `version` in all three manifests, commit, and refresh the
   marketplace (see `docs/plugin-workflow.md`).

Standard pattern (also documented in per-skill `README.md` when vendored):

```bash
npx skills add <owner>/<repo> -y --skill <skill-name>
cp -R .agents/skills/<skill-name>/* skills/<skill-name>/
trash .agents/skills/<skill-name>
```

The trailing `trash` matters: `.agents/skills/` is **tracked** — it holds this repo's
internal skills, and `.claude/skills` symlinks to it. A download left behind there
shows up as an untracked directory with no `SKILL.md`, which `bun run validate`
warns about. Never commit one.

## Adding a new skill

When creating or vendoring a skill:

1. Add/edit files under `skills/<name>/`.
2. **Add an entry to `skills/sources.json`** — every skill gets one:
   - `local` if authored here
   - full upstream + `refresh` if vendored, then
     `scripts/check-upstream.sh --record <name>` to pin `upstreamRev`
3. For vendored skills, add `skills/<name>/README.md` with the same refresh one-liner.

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

**Origin breakdown (2026-08-28):** 13 vendored · 8 adapted · 6 companion · 1 derived · 8 local (36 total).
21 of these (all `vendored` + `adapted`) carry an `upstreamRev` pin.

## Related

- [`docs/plugin-workflow.md`](plugin-workflow.md) — edit → publish loop, why edits are not live
- [`docs/supported-agents.md`](supported-agents.md) — where each runtime installs skills
