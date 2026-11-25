# create-formal-verification-skill

Adapted from [cursor/plugins](https://github.com/cursor/plugins)
(`pstack/skills/create-formal-verification-skill`).

Finds the part of a repo where a bug costs the most and tests reach the least
(races, retries, state machines, parsers, unsafe code), verifies one property of it
with whichever tool fits (a model checker such as TLA+, an SMT-backed verifier, a
prover, or generated-input testing when nothing runs on the language), and leaves a
project-local `verify-<area>-formal` skill that rechecks it. It shows each property
failing on a broken variant before trusting a pass.

Paired with `maintain-formal-verification-skill`, which brings the verification back
in line after code changes that skipped it. Sibling of `create-verification-skill`,
which proves behavior by driving the running app; this one checks a property over
every case in a stated scope, or, when it falls back to generated inputs, over a
reported sample of them.

## What changed

- Writes the generated skill to `.agents/skills/` (with `.claude/skills` as a
  symlink), as `create-verification-skill` does, instead of an unspecified location,
  and names it `verify-<area>-formal`.
- Upstream sends TLA+ results through pstack's `/statechart` skill, which this
  plugin does not ship. The generated skill instead retells a violation as the
  shortest sequence of steps in the code's words and states what a pass covers.
- The check runs through one pinned command in the project's own tooling.
- `agents/openai.yaml` is a local addition so Codex honors the same user-invoke-only
  policy as `disable-model-invocation`.

To update:

```bash
npx skills add cursor/plugins -y --skill create-formal-verification-skill
# hand-merge this adapted copy; never overwrite it
```
