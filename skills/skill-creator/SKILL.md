---
name: skill-creator
description: "Create, revise, and evaluate skills, including descriptions, supporting resources, triggering, and output quality."
---

# Skill Creator

Create, revise, and evaluate skills for the intended tasks and runtimes.

Start at the user's current stage: clarify missing intent, draft, revise, or
evaluate. Use existing decisions and preserve review-only/no-commit boundaries.
A skill states the goal, completion condition, constraints, safe failure direction,
and facts the agent cannot derive locally. Keep task-specific recipes in references.

Descriptions should name the real task, distinctive capability, and important
exclusions concisely. Do not make unrelated prompts trigger to compensate for a
particular model. Preserve explicit-only invocation policy and existing metadata.

For changed behavior, use representative positive requests and close negative
matches, plus a baseline when useful. Evaluate observable outcomes and constraints;
do not score only wording or token count. Use fresh contexts on intended available
hosts/models. If subagents are unavailable, evaluate sequentially and disclose the
lack of independent context. Report untested host coverage honestly.

The bundled trigger optimizer is Claude-specific: it uses Claude CLI and the
Anthropic API. Its explicit model must be compatible with both; a GPT session's
model ID cannot be forwarded. It does not prove Codex triggering. Read that
reference only when running this optimizer. All bundled helper paths are anchored
to the absolute directory containing this skill's SKILL.md in the same shell call.

## Communicating with the user

The skill creator is liable to be used by people across a wide range of familiarity with coding jargon. If you haven't heard (and how could you, it's only very recently that it started), there's a trend now where the power of Claude is inspiring plumbers to open up their terminals, parents and grandparents to google "how to install npm". On the other hand, the bulk of users are probably fairly computer-literate.

So please pay attention to context cues to understand how to phrase your communication! In the default case, just to give you some idea:

- "evaluation" and "benchmark" are borderline, but OK
- for "JSON" and "assertion" you want to see serious cues from the user that they know what those things are before using them without explaining them

It's OK to briefly explain terms if you're in doubt, and feel free to clarify terms with a short definition if you're unsure if the user will get it.

---

## Reference files

The agents/ directory contains instructions for specialized subagents. Read them when you need to spawn the relevant subagent.

- `agents/grader.md` — How to evaluate assertions against outputs
- `agents/comparator.md` — How to do blind A/B comparison between two outputs
- `agents/analyzer.md` — How to analyze why one version beat another

The references/ directory has additional documentation:
- `references/schemas.md` — JSON structures for evals.json, grading.json, etc.

## Task references

Read the reference for the task at hand; do not load every recipe.

- [Authoring](references/authoring.md): capturing intent, writing a skill, creating UI metadata, and drafting representative tests.
- [Evaluation](references/evaluation.md): paired output evaluations, assertions, timing, grading, and the viewer.
- [Iteration and comparison](references/iteration-and-comparison.md): improving a draft from evidence or running blind comparisons.
- [Claude trigger optimizer](references/claude-trigger-optimizer.md): Claude CLI/Anthropic API trigger optimization and optional packaging.
- [Host adapters](references/host-adapters.md): Claude.ai or Cowork-specific capability limits.
