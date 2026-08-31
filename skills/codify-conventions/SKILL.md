---
name: codify-conventions
description: "Codify a repo's conventions and enforce them with lint config and pre-commit hooks. Two modes: audit the codebase for de-facto patterns worth codifying, or grill the user on rules they want declared. Creates and maintains a CONVENTIONS.md of rules, wires the enforceable subset into linters and hooks, and makes adding a new rule a one-step affair. Use when the user mentions conventions, code style, lint setup, pre-commit hooks, 'how do we do X in this repo', 'make the linter catch this', or 'stop people from committing Y' — even if they don't name a linter or hook manager."
---

# Codify conventions

Turn the way a repo actually behaves into rules someone — a linter, a hook, or a
reviewer — actually checks. A convention nobody enforces is a wish; this skill
gives each rule a place where it is enforced or at least seen.

Two entry points, one artifact:

- **Audit mode** (default when nothing is codified yet): read the code, find the
  patterns that already hold, propose codifying them.
- **Grill mode** (when the user has opinions the audit cannot see): interview
  them rule by rule, using the interview technique from `grilling`.

Both converge on the same artifact and the same enforcement wiring. Confirm
before writing anything; every rule lands with the user's yes.

## The artifact: `CONVENTIONS.md`

Project-root `CONVENTIONS.md`, created **lazily** — never pre-create it empty.
An empty conventions file gets read, believed, and found empty; create it only
when the first real rule lands. It holds two classes of rule, clearly separated:

1. **Enforced by tooling** — the linter or hook catches violations. Each rule
   names where it is enforced (config file + rule id).
2. **Judgment calls** — a linter cannot catch it, so a reviewer or agent must.
   Write these as a checkable question, not a vibe: "error messages name the
   failing operation, not just 'something failed'", not "good error messages".

Never drop a rule silently because no linter supports it. Judgment rules exist
so that nothing the user cares about goes unseen.

One rule per line where possible. Each rule states what to do, not what not to
do, and links to an example commit or file when one exists.

## Mode 1: Audit

The repo already follows conventions; the audit's job is to notice them and
distinguish convention from accident.

1. **Sample broadly**: recent commits (`git log` + diffs), file and directory
   naming, error handling, test layout, comment style, import ordering, commit
   message shape. Whatever the stack suggests — read its idioms from the code,
   not from a style guide you remember.
2. **Find patterns that hold**: a rule is a candidate only if it holds in the
   strong majority of the code. If it holds half the time, it is not a
   convention yet — it is a choice the user gets to make, which is grill-mode
   material.
3. **Distinguish convention from accident**: three files doing the same thing
   by coincidence is not a convention. Look for repetition across authors,
   across time, and in code that was deliberately written (config, README,
   scripts) versus incidental.
4. **Propose**: present candidates as a table — pattern, evidence, enforceable
   now or judgment call, proposed enforcement. The user strikes and amends;
   nothing is written until they say so.

Audit mode never invents rules the code does not follow. If the user wants the
code to *start* behaving a certain way, that is a new rule — mark it as such so
they know it will fight existing code, and offer to fix the existing violations
in the same pass.

## Mode 2: Grill

When the user arrives with opinions ("I want X caught at commit time"), or when
the audit leaves gaps only they can fill:

- One question at a time, concrete examples over abstractions: "when a function
  can fail three ways, do you want one error type or three?"
- For each answer, classify immediately: enforced-by-tooling or judgment call.
- Batch-confirm before writing: show the full rule list, let them strike and
  amend, then write once.

## Enforcement wiring

Wire it here — this skill owns the whole path from rule to hook. But wire what
the project already has; do not import an ecosystem.

1. **Inventory first**: which linters, formatters, and hook managers does the
   project already use (check lockfiles, config files, package scripts)? Which
   package manager? A project on Ruff does not get ESLint; a project with no
   hook manager gets the lightest wiring its ecosystem supports, or — for
   language-less repos — a plain script under `.githooks/` enabled with
   `git config core.hooksPath .githooks`.
2. **Map rules to enforcement**: each enforceable rule becomes a specific
   linter rule, a hook check, or a small bundled script. If a rule is not worth
   the wiring, say so and leave it as a judgment rule — visible beats enforced-
   badly.
3. **Wire without clobbering**: add to existing config, never replace it. Show
   the diff before writing. If a proposed rule contradicts an existing linter
   rule, surface the contradiction — the user resolves it, not you.
4. **Verify the enforcement actually fires**: commit a deliberate violation on
   a scratch file, watch the hook block it, then revert and trash the scratch
   file. A hook that has never blocked anything is decoration. Report what you
   verified.
5. **Degrade loudly**: where a runtime skips hooks (`--no-verify`) or a check
   cannot run, say so in the artifact — a rule enforced 80% of the time is
   still worth having, but the user should know which 20% it misses.

## Adding a rule later

The common case, and it must stay cheap:

1. User states the rule (or a violation annoys them).
2. Classify: tooling or judgment.
3. Add one line to `CONVENTIONS.md` under the right heading, wire the
   enforcement if tooling, verify it fires.
4. Done — no re-audit, no re-interview.

When run in a repo whose `CONVENTIONS.md` already exists, start from step 1 of
this section, not from the audit — the conventions conversation already
happened; extend it.

## Verify

- Every rule in `CONVENTIONS.md` is either wired into tooling or written as a
  judgment rule. Nothing orphaned, nothing dropped.
- The hook blocks a real violation (tested, not assumed).
- The existing lint setup still passes — codifying conventions must not turn a
  green repo red.
