---
name: why
description: "Use when asked 'why X works this way' kind of questions. Investigate design rationale, historical decisions, regressions, and thresholds using cited evidence. Use how for runtime behavior."
---

# Why

Find the evidence behind a design decision, regression, or threshold. `how`
explains mechanics; this skill explains motivation without inventing intent.

## Follow the evidence

1. Anchor the question in the relevant code, symbol, decision, or incident. Use
   the current conversation to resolve obvious context; ask only for a material
   missing target. Inspect local history, linked PRs, ADRs, or the source the user
   named through the available tools.
2. Answer a narrow question directly when a reliable explicit record supplies
   the answer and there is no unresolved contradiction. Verify that the record
   applies to this version and scope. Do not search every system by ritual.
3. Expand when the record is missing, indirect, conflicting, or the user asks for
   broad investigation. Use [investigation planning](references/investigation-planning.md)
   to select useful evidence categories and delegate independent inquiries when
   supported. Use configured available models and supported host arguments;
   otherwise investigate inline. Keep the work read-only.
4. Reconcile evidence before writing the narrative. Surface competing explanations
   and contradictions. Code describes behavior; it rarely proves motivation.

## Evidence standard

Cite each factual claim about intent to a commit, PR, ticket, document, chat
permalink, or explicit source comment. Distinguish direct evidence from inference
and calibrate language to confidence. A failed search means no matching record
was found in that search, not that a decision was never documented or ticketed.
Do not infer intent from today's code shape or confirm the user's hypothesis
without checking it.

Read [epistemics](references/epistemics.md) for indirect evidence, conflicting
accounts, or a substantial historical synthesis. Keep its confidence distinctions
when presenting a delegate's answer; do not remove hedges for smoother prose.

## Result

Lead with the supported answer. Include relevant code anchors, direct evidence,
labeled inference, competing hypotheses when unresolved, and concrete gaps.
Scale the format to the question. For a broad investigation, show sources
consulted, searches with no relevant results, and unavailable sources so the user
can assess coverage. Never imply an unsearched category was checked.

If the question precedes a requested code change, translate the findings into
preserve / change / avoid / risk constraints for that work. An explanation alone
does not authorize implementation.

## References

- [Investigation planning](references/investigation-planning.md): source selection, the seven-category roster, and optional delegation.
- [Source playbooks](references/source-playbook.md): query recipes for the selected source category.
- [Incident playbook](references/sources/incident-postmortem.md): defensive code or suspected incident history.
- [Investigator prompt](references/investigator-prompt.md): a bounded delegated inquiry.
- [Synthesizer prompt](references/synthesizer-prompt.md): a substantial delegated synthesis.
