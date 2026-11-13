---
name: learn-from-miss
description: "Turn a caught mistake into a proven guardrail so the same miss never reaches a human twice. Use after an accepted review comment, a CI or production failure the review let through, a bug found after merge, or a correction you have now made twice."
---

# Learn From Miss

A **miss** is a mistake that got past every check that should have stopped it and was caught later: a review comment someone accepted, a CI or scheduled-job failure caused by the change, a bug found after merge, a correction the user had to give again. Every miss either becomes a **guardrail** that catches the next one before a human sees it, or is recorded as a one-off. Text that asks an agent to remember is the weakest guardrail; reach for it last.

Inputs, per miss: what was caught, where (link to the comment, log, or report), the **fix** (the commit or diff that resolved it), and the **miss commit**, the state where it should have been caught. For a review comment that is the PR head the comment was left on, with the PR's merge base as **base**. For a post-merge bug it is the commit that introduced the bug (blame or bisect) and its parent. A caller that already holds these passes them; otherwise derive them before step 1.

## 1. Decide whether there is a lesson

- **One-off**: a typo, a local slip, a wrong value with no rule behind it. The fix is enough. Record nothing and stop.
- **Already guarded**: a check, standard, or instruction already covers this. Then the guardrail exists but was not loaded or not followed, and that is the finding: fix it one rung above the existing guardrail.
- **Lesson**: anything else. Write it as a *general* rule ("dedupe at the declared key"), never as a hint about this case ("check `orders.id`"). A rule that only fits this case catches nothing next time.

## 2. Climb the ladder

Try the rungs from the top. Take the first one that genuinely prevents the miss; the stronger the rung, the less any future agent has to remember. Agents copy whatever the surrounding code does, so a weak guardrail becomes the next template.

1. **Codebase.** Change the design so the mistake has nowhere to live: a deeper module that owns the invariant, an interface that makes the wrong call unrepresentable, a type that rejects the bad state, one owner instead of hand-synced copies, the old way deleted. This is the best rung and the rarest. It is a design change, not a test. Use `codebase-design` for the interface criteria and `refactoring` to carry it out without changing behaviour.
   **Proof:** show that the miss can no longer be expressed. Re-apply the original mistake on top of the change and watch it fail to compile, fail to import, or have no place to go.
2. **Static analysis.** The mistake is a pattern a machine can spot: a custom lint rule in the project's own linter, a check script, a CI job, a schema or contract test. Its error names the fix ("use `X` instead"). When the pattern is already common, fail only on changes that add more of it. Add a test only when the behaviour itself is what broke and no lint can see it; a test per miss bloats the suite without raising the floor.
   **Proof:** red on the miss commit, green on the fix, run by the same command locally and in CI.
3. **Prose.** Only judgment can catch it. Edit the context the next agent reads: `CODING_STANDARDS.md` when the **reviewer** should catch it, or the project's agent instructions, a skill, or a doc when the **author** should avoid it. Place the rule where the agent that needs it reads it, and keep it general.
   **Proof:** an **eval case** that is red before the edit and green after, plus every existing case of the same reader still green. `references/evals.md` owns the case format, the replay for each reader, and grading. Read it before writing a case.

A rung without its proof is a proposal, not a guardrail.

## 3. Land or propose

- **Proven** guardrails are committed with the work that triggered the miss, as their own commit, so the reviewer of that work sees them beside the code. A codebase-rung change that reaches past the fix's own module boundary is a proposal regardless of proof: it belongs in its own change.
- **Unproven** guardrails, and every new CI job or repo-wide rule that fails changes other people make, go to the user for approval with the draft and the evidence so far. Apply them only after a yes.

When invoked with `mode:pipeline` (an unattended caller resolving PR feedback), never block on a question. Act within the caller's inherited scope: commit proven guardrails to the work's head, and return everything else as proposals for the caller's report.

## 4. Report

One line per miss: the lesson, the rung, the guardrail (file and rule, or eval case path), the proof (command and red/green result), and whether it landed or awaits approval. One-offs are counted, not listed.

Done when every miss handed in is a landed guardrail, a proposal with evidence, or a counted one-off.
