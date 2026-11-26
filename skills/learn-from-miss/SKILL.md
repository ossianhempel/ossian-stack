---
name: learn-from-miss
description: "Encode a guardrail after a fixed defect or rule break slipped past existing checks — PR review feedback fixed, a diagnosed bug or post-merge failure, a recurring autoreview miss, or 'make sure this never happens again'. Picks the cheapest guardrail that holds (type, check, test, or review rule) and proves it."
---

# Learn From Miss

A finding caught after existing checks passed is one our guardrails missed. Close the class with the cheapest durable guardrail that holds, then prove it catches the miss.

Run after the fix exists.

## Inputs

Take one or more fixed findings, each with:

- the file, lines, and what was wrong;
- the **miss commit** (when replay or historical check verification is needed):
  - Inline PR review comment: the reviewed commit (`originalCommit.oid` on GitHub, or the iteration source commit on Azure).
  - Review submission body: the reviewed commit (`commit.oid`).
  - Top-level PR comment: the PR head at comment time if known, else the newest PR commit preceding `createdAt`.
  - Diagnosed bug or post-merge failure: the pre-fix commit confirmed by the debugger's reproduction (inspecting that pre-fix revision, not the fixed lines, if attributing an earlier introducing commit).
  - Pre-push review finding: the pre-fix state where local checks passed.

Verify any historical miss commit reproduces the reported failure before using it as a red baseline. If the commit cannot replay the failure cleanly (for example, an unpushed commit timestamp mismatch or shifted context), prove the guardrail red-then-green with a focused test reproducing the bad pattern instead, or report it as not replayable.

## Qualify

Take a finding only when all hold:

- it was **fixed** (not declined, dismissed, or awaiting a human decision);
- it is a **defect or rule break visible in the change**, not a typo, formatting preference, or an undecided product/business rule. If nobody has decided the rule, stop and surface it to the user rather than guessing;
- it represents a **repeatable class or missing check**, not a one-off local slip that the fix and its regression test already cover.

## Route

Inspect what the repository already has first (active instructions, linter config, typecheck, test harness, hooks, CI workflows, `CODING_STANDARDS.md`, and any project-local review skills or evals). Never reinvent a check that already exists unwired — wiring or fixing an existing check is the win.

Pick the first rung that prevents the class without false positives:

1. **Project-local guardrail or eval harness.** If the repo already maintains a custom convention checker, lint plugin, review eval suite, or local learning workflow in its active instructions, extend that mechanism instead of creating a parallel one.
2. **Type or boundary.** Tighten a type, signature, or module boundary so the bad state fails to compile or typecheck — only when the change stays small and within the current task's scope. If the right structural fix would turn a narrow change into a broad refactor, do not widen the diff; record it as a follow-up proposal and either drop to the next rung or stop.
3. **Deterministic check.** The finding breaks a mechanical rule (banned API, import boundary, missing flag/annotation, syntactic pattern, schema/manifest drift, file-location rule) that code can detect cleanly.
   - Add the rule to the repo's existing linter, custom check script, hook, or CI check, with an error message naming what to use instead.
   - If pre-existing code violates the rule, add a ratchet/baseline or scope it to changed files rather than sweeping unrelated code here.
   - **Prove it fails on the miss** (a failing unit test of the rule reproducing the bad pattern, or running the check against the miss commit) and passes on HEAD.
4. **Behavior test.** No static check catches the class, and the fix does not already lock down the observable behavior class at the right seam. Apply `principle-test-behavior-not-implementation`, add the focused test, and prove red on the miss and green on the fix.
5. **Review or guidance surface (judgment calls only).** The miss requires judgment no check or test can substitute for (cross-file consistency, architectural boundary, unwritten domain convention):
   - If the repo ships a project-local review prompt and eval suite, add a regression eval case on the miss commit, replay it once (without showing the reviewer the expectations), close any miss at its cause (missing doc vs reviewer prompt without naming case-specific files), and rerun once; a second miss goes to the user with both outputs.
   - Otherwise place the rule in the narrowest review-time surface the repo uses (`CODING_STANDARDS.md`, path-scoped instructions, a domain doc, or `GLOSSARY.md`), keeping always-loaded project instructions as a single pointer line of last resort.
   - If a text rule already existed and was still missed, raise it to a higher rung (check, type, or test) instead of adding more text — or report why it could not be raised.
6. **Skip.** A one-off defect with no generalizable rule behind it. The fix is enough; say why in one line.

## Scope and commits

- **Honor caller authority.** Inherit the enclosing task's commit, push, and scope limits. In diagnosis-only or read-only runs, propose the guardrail without editing or committing.
- **Stay bounded in unattended or frozen contexts.** Under unattended pipeline mode or release-freeze branches, commit only small, proven, low-risk guardrails (a targeted check test, focused lint rule, eval case, or narrow standards/doc update). Surface broader refactors or undecided policies as proposals for the user instead of committing them.
- **Separate commit.** When committing, keep guardrail changes in their own commit(s) apart from the fix (`feat(ci): ...`, `chore(lint): ...`, `test: ...`, or `docs: ...` per the repo's commit conventions) so reviewers can inspect or revert them independently. Push with the caller's push.
- **Protect existing guardrails.** Never loosen an existing check or baseline entry here. For a new repo-wide linter or CI check: on a PR branch, flag it explicitly for human approval before merge; on a direct trunk push with no PR merge gate ahead, defer it as a proposal (or ask first) unless already authorized.

## Report

For each finding: route taken (local harness, type, check, test, guidance, or skip), exact guardrail added (or why skipped), proof result (red-then-green or replay outcome), and anything needing a human (a repo-wide check to approve, a structural follow-up too large for this change, an undecided rule, or a replay that still missed).
