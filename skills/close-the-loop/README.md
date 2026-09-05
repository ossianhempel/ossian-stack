# close-the-loop

Adapted from [cursor/plugins](https://github.com/cursor/plugins)
(`pstack/skills/create-verification-skill`).

Generates a project-local verification skill: launch the real app, health-check
it, drive a feature the way a user would, capture evidence, tear down. Plus a
feature map so later runs know what else needs proving. It runs its own output
end to end once before handing it over — an unexecuted generated skill is a
draft, not a deliverable.

Paired with `maintain-close-the-loop`, which keeps the map honest as the app changes.

## Why the rename

Upstream calls it `create-verification-skill`. Renamed to Ossian's own vocabulary:
verification is the mechanism, closing the loop is what it achieves. Per the vault
note, an agent without a check hasn't got a loop — it has repeated prompting. The
upstream wording is kept in the description so both vocabularies trigger it.

Slight over-claim to know about: closing the loop also covers the stop condition
and the feed-forward memory that makes iterations compound. These two skills build
and maintain only the checking half.

## What else changed

Upstream hardcodes `.cursor/skills/verify-<app>/`. A new step 0 resolves the
project's own skills directory instead — first existing of `.agents/skills/`,
`.claude/skills/`, `.cursor/skills/`, else create `.agents/skills/` and symlink
`.claude/skills` to it, since Claude Code does not read `.agents/skills`. The
cross-reference to `/maintain-verification-skill` now points at
`/maintain-close-the-loop`.

`agents/openai.yaml` is a local addition so Codex honors the same user-invoke-only
policy as `disable-model-invocation`.

To update:

```bash
npx skills add cursor/plugins -y --skill create-verification-skill
# hand-merge; this copy is renamed and adapted, never overwrite
```
