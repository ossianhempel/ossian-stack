# Pickup loop prompt

The runner for autonomous ticket pickup is the host's recurring-prompt facility,
not a skill: Claude Code's and Cursor's built-in `/loop`, or a scheduled routine
in the desktop app. Codex has no loop built in; a scheduled routine or a shell
loop around `codex exec` does the same job. Paste the prompt below as the loop
body, e.g. `/loop 30m <prompt>`. Adjust the interval to how often new
`ready-for-agent` tickets appear.

---

Read the project's issue-tracker config, triage-label mapping, ticket brief, and
handoff-comment policy from `docs/agents/`. Resolve every triage role through
the mapping (`docs/agents/triage-labels.md`); the names below are the canonical
defaults. Then run the tracker config's **Pickup operations** once. Run only one
loop per repo and project: overlapping runners serialize on claim-comment order,
not on owner fields.

If `docs/agents/jira-mapping.md` exists, an exact `pickup.*` row overrides
only that operation. Missing rows keep the tracker template's original query,
claim, blocked, paused, and done behavior.

1. Use the exact `pickup.frontier` operation when present. Otherwise query the
   default frontier: tickets in the agent-ready triage role, unclaimed, not
   blocked, oldest first. If it is empty, report "no work" and stop.
2. Use the exact `pickup.claim` operation when present. Otherwise claim the first
   one with the default protocol: post the claim handoff comment stating
   `<runtime>:<session-id>` first, set the owner field, then re-read comments and
   owner. The owner field alone is last-writer-wins, so the winner is the earliest
   claim comment, not the field value. If another session's claim comment is
   earlier, release the claim and take the next ticket.
3. Read the ticket/spec, relevant ownership/handoff history, and linked evidence;
   a minimal latest claim comment is not the full context. Work from the brief.
   Verify against the real artifact using the
   brief's Verify section. Follow the project's branch and worktree convention
   (the brief's Scope names it; project instructions in context win): only create
   a ticket-named branch where the project does that.
4. Comment only on meaningful progress, a new or changed blocker, a decision
   needed, or completion. Use a few sentences with evidence links; omit empty
   sections. Do not repeat unchanged blockers or mirror HQ/agent coordination.
   Preserve the required claim/release records and recovery pointers. On a question
   only a human can answer, use the exact `pickup.blocked` operation when present;
   otherwise state it concisely, record the release and resume context, release
   the claim, and stop. On completion, use the exact `pickup.done` operation when
   present; otherwise open the PR, post a concise acceptance/evidence summary,
   move the ticket to review, and stop. Keep accepted decisions in the ticket/spec
   and link detailed evidence.
5. Never relax the acceptance criteria to finish. Never take a second ticket in
   the same run.

Report: the ticket taken, the final status, and the PR or the open question.
