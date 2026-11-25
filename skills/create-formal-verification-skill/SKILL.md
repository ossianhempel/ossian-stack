---
name: create-formal-verification-skill
description: "Generate a project-local skill that formally verifies the code where a bug costs the most and tests reach the least, in any language, with whichever verification tool fits. Use for /create-formal-verification-skill, \"model-check this race\", \"prove this invariant\", or when concurrency, retries, state machines, parsers, or unsafe code need more than tests."
disable-model-invocation: true
---

# Create a formal verification skill

A test checks the cases that someone thought to write. Formal verification checks every case in a stated scope: every order of steps in a model, every input up to a bound, or every input. This skill finds the part of the repo where that matters most, verifies one property of it, and leaves a project-local skill that lets the next agent check a change against that property. Write that skill for an agent who reads it cold, mid-change, and has never seen your work. The user must be able to trust the result and act on it without learning the verification language.

## Resolve where project-local skills live

One tree serves every runtime, and it is `.agents/skills/`. Codex and Cursor read it directly; Claude Code reads it through a symlink. Write the generated skill there and nowhere else:

- `.agents/skills/` exists: use it.
- It does not: create it, even when `.claude/skills/` or `.cursor/skills/` already exists as a real directory. A copy there is invisible to the other runtimes and drifts from the original.
- `.claude/skills` is a symlink to `.agents/skills`, never a second tree. Create the symlink when it is missing. If it already exists as a real directory holding its own skills, stop and tell the user: migrating it is their call.

Name the generated skill `verify-<area>-formal` (the area in this repo's own words), so it sits beside any `verify-<app>` skill without colliding. Say which directory you resolved, once, before you write.

## Choose the target from the code

Answer from the codebase, and ask the user only what you cannot observe. If the user named an area or a bug, start there.

A good target is a promise the code makes, where a break harms users and tests rarely reach the case that breaks it. Choose the strongest such target in the repo, not the one that is easiest to verify.

## Let the question choose the tool

Pick the tool that answers the question at the lowest cost: a model checker, a proof assistant, an SMT-backed verifier, or another tool. Whether events can happen in a bad order usually suits a model checker over a small model of the design, and TLA+ is the default for that in any language. Whether the code itself behaves for every input, as with memory safety, overflow, or a data-structure invariant, usually suits a verifier that runs on the code. If no verifier runs on this language, say so, and test the real code with generated inputs, not a hand model of the function. A property that must hold at every size, where a bound is not enough, can need a proof. Prefer a tool that the repo's developers can install and run, and tell the user why you chose it. Pin its version and wrap it in one command in the project's own tooling (a package script, a Makefile target, `scripts/verify-<area>-formal`), not a new toolchain, so the check runs the same way for every agent and from the project's local check command.

## What makes it good

- **True to the code.** Every part of the model or proof points to code that a reviewer can open. What the verification treats as one indivisible step is one indivisible step in the code. Names come from this repo.
- **Able to fail.** A check that you have never seen fail proves nothing. Show each property failing on a broken variant of the code it guards, such as a removed check or a reordered step. A verifier that runs on the code sees that break directly. A separate model (TLA+) does not: make the same break in the model, in the action that stands for the changed code, and confirm the checker fails on it.
- **Findings stay findings.** When the current code breaks the property, report it with the counterexample in the code's terms. Do not weaken the property or the model until it passes, and do not change product code unless the user asks.
- **Honest about scope.** Say what is verified, under which bounds and assumptions, and what is left out. A pass covers the model or the bound, not the whole system. Generated-input testing samples its bound and never covers it: report how many inputs ran and how they were drawn, and never call that pass exhaustive.
- **Readable without the tool.** State the property and the harm in one plain sentence each. Tell a counterexample as a short sequence of steps in the code's words.
- **Cheap to rerun.** One command, a reproducible tool version, and a run short enough that the next agent will use it on every relevant change.
- **Kept in step with the code.** Record which files and functions each check covers, and the commit at which you last confirmed that the verification describes them. When the covered code changes after that commit, the next agent can see that the verification needs another look.

## Generate the verify skill

Write a project-local skill with frontmatter that names the area and says when to use it. Without frontmatter, the skill never registers. From the skill alone, the next agent must be able to tell whether a change touches the verified code, run the check, tell a real bug from a modeling error, and update the verification when a change is intended. Put the coverage record and the sync commit in the skill, and tell the next agent to move the sync commit forward only after it confirms that the verification describes the code at the new commit. When the verification describes covered code that is not committed yet, the sync is pending (no commit) until that code is committed and rechecked. Use this repo's real commands, paths, and nouns, and leave no placeholders.

If the check is a state model (TLA+ or another model checker), tell the next agent how to read its results:

- **Violation:** the checker's trace is the counterexample. Retell it as the shortest sequence of steps in the code's words, each step naming the function or handler it stands for, ending in the state that breaks the property. Never hand the raw trace to the user.
- **Pass:** say which states and steps the model covers and the bounds it explored, so a pass is never read as "the system is correct".

Write the model's actions as named steps that match the code (`ClientRetries`, `WorkerAcksJob`), not one anonymous `Next`, so a trace reads as code.

## Prove it before you hand off

Follow the generated skill once, as the next agent would, on a scratch change that breaks the property in the real code. Make it in a disposable copy (a scratch git worktree with the current uncommitted changes applied, including the verification you just generated), never in the user's checkout, and tell the generated skill to do the same. Run the check there once before the break, so you know the copy starts where the checkout does. It must catch the break. When the check runs on a separate model, the skill must lead the next agent to see that the scratch change alters a modeled step, mirror it in the model, and get the failure there; a model that keeps passing because it never read the change is the miss this step exists to catch. Then drop the scratch change and confirm that the check is back where it started: passing, or failing only on the findings you will report. A verify skill that was never run is a draft. If the skill misses the break or a step does not run, fix the skill or the verification, not the scratch change.

## Hand off

Tell the user what you verified, which tool you used and why, the bounds, what the check found in plain words, how to run it, and what it does not cover. Suggest a second target only if you found a close one. Point the user at `/maintain-formal-verification-skill` for bringing the verification back in line after changes that did not recheck it.
