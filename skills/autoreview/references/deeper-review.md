# Deeper Review

Use when changed behavior has serious failure consequences or unresolved
cross-boundary assumptions. Autoreview remains the sole review-and-fix loop;
this reference changes the inputs and depth of a pass.

## Select the depth

Name the consequential failure and the boundary that could produce it. Changes
to data preservation, migration compatibility, access or ownership, money,
concurrent state, retries, or recovery warrant a focused brief. A wording change
on a payment screen does not by itself change the payment contract.

Start with the configured single reviewer. Use the existing panel when a failure
would cause serious loss or exposure, or an unresolved assumption needs a second
independent judgment. Each panel member receives the same frozen bundle and
brief and reports all actionable findings in one pass. State the reason for the
extra reviewer; the skill does not delegate ordinary implementation.

## Prepare the brief and evidence

Give the reviewer enough context to challenge the change:

- **Contract:** intended observable behavior and invariants that must survive.
- **Scope:** original request, owner boundary, reviewed revision or local snapshot,
  and relevant callers, persisted formats, or external contracts.
- **Failure questions:** realistic sequences that might violate the contract,
  such as interruption between persistence and acknowledgment or a retry after
  success. Questions are hypotheses, not asserted defects.
- **Evidence:** focused test results, representative inputs, and which behavior
  they actually exercise. Distinguish executed proof from source reasoning and
  checks still unavailable.
- **Previous findings on a rerun:** accepted findings, fixes, retest evidence,
  rejected findings with reasons, and unresolved questions. Keep these advisory:
  reviewers independently check the current change for new defects too.

Pass a short brief with the helper's existing `--prompt`, or put a longer one in
a repo-relative file passed with `--prompt-file`. Supply necessary unchanged
source or test evidence through explicit repo-relative `--dataset` files. Select
the relevant context; all input retains the helper's scanning, redaction, size,
and isolation checks. Reviewers cannot read the working repository, and adding a
brief does not grant repository access or permission to execute tests. Temporary
briefs and evidence stay outside the delivery diff.

For example, reviewing an older client's write path against a newer persisted
format needs the decoder, write boundary, and representative record envelope.
Ask whether unreadable records survive a write attempt; an internal decoder-flag
assertion alone does not prove that behavior.

## Evaluate findings in the existing loop

A finding needs a realistic trigger, expected and actual behavior, a precise
location, and supporting evidence. A reproduction is strongest; a complete
source trace can also demonstrate a defect. Label untested assumptions and
missing evidence explicitly. Do not invent a defect because context is absent.

The main agent verifies findings, classifies their scope, implements accepted
fixes, and runs focused proof. For important regressions, show that the test fails
for the original defect or a deliberate local break, then passes with the fix.
Use a disposable copy for deliberate breaks; preserve unrelated working changes.

If a concrete question cannot be resolved from the bundle, the main agent
investigates it. A focused investigative subagent is optional when independent
exploration is useful. It reports once, may use an isolated scratch reproduction,
and leaves product edits and integration to the main agent. Keep shared devices
and live verification under one driver. A read-only prompt is not a sandbox;
honor the host's actual permissions and the original task's scope.

Feed the resulting evidence back into the next helper pass. After a code change,
review the updated complete target with the selected reviewer configuration and
rerun affected proof; earlier clean results do not cover later edits. A merge,
rebase, or cherry-pick that changes the delivered content also needs affected
proof and review of that result.

The existing scope governor still applies: after two correction cycles without
convergence, reclassify remaining findings before editing again. Continue only
for in-scope blockers. A failed or partial panel is incomplete review, not a clean
result. Once the selected review completes with no accepted actionable findings
and the required behavior proof passes, stop. Another reviewer needs new evidence
or a newly identified risk, not a desire for reassurance.
