---
name: to-spec
description: Turn the current conversation into a spec and publish it to the project issue tracker — no interview, just synthesis of what you've already discussed.
disable-model-invocation: true
---

This skill takes the current conversation context and codebase understanding and produces a spec. Do NOT interview the user — just synthesize what you already know.

The issue tracker and triage label vocabulary should have been provided to you — run `/setup-ossian-stack` if not.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one.

Check with the user that these seams match their expectations.

3. Write the spec using the template below, then publish it to the project issue tracker. The template emits the project's ticket brief sections directly (Goal, Scope, Context, Acceptance, Verify, Forbidden, Blocked by, in that order where the spec shape allows), so a cold pickup agent can start from the published body with no translation. Apply the `ready-for-agent` triage label only when every brief section is filled — a field you cannot fill is a spec that is not ready. Resolve the label through `docs/agents/triage-labels.md` when the project maps it to a different string.

<spec-template>

## Goal

One or two sentences. The outcome from the user's perspective, executable by a stranger. Distills the Problem Statement and Solution below into the ticket-brief Goal.

## Scope

What the implementation may change and what it must not. Name modules, areas, or surfaces in the project's domain vocabulary, not file paths. State the branch or worktree convention if the project has one.

## Context

Pointers, not prose: the parent issue or conversation this spec came from, related ADRs, the prototype that settled a decision, prior tickets this builds on. Paste in anything a cold agent needs that lives only in this conversation.

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature. Stories alone are not acceptance: every story must distill into at least one checkable box under Acceptance below, and dependency edges go under Blocked by, not in story prose.

## Acceptance

Checkable criteria, one per line, as a task list. The ticket is done when every box is ticked against the real artifact, not a self-report. Derive them from the user stories above; a story with no box is an untestable story.

- [ ] …

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Verify

The exact commands, or the project's verification skill, that prove the feature works, plus known gotchas. A pickup agent runs these before calling the work done.

## Forbidden

Actions the implementation may not take beyond the project's standing rules: no migrations, no dependency bumps, no changes outside the modules named above.

## Blocked by

References to the tickets that gate this spec, or `None — can start immediately`. Use the tracker's native blocking relation as well where it has one. Never leave a known dependency in prose only.

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
