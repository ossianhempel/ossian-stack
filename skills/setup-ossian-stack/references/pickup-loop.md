# Pickup loop prompt

The runner for autonomous ticket pickup is the host's recurring-prompt facility,
not a skill: Claude Code's and Cursor's built-in `/loop`, or a scheduled routine
in the desktop app. Codex has no loop built in; a scheduled routine or a shell
loop around `codex exec` does the same job. Paste the prompt below as the loop
body, e.g. `/loop 30m <prompt>`. Adjust the interval to how often new
`ready-for-agent` tickets appear.

---

Read the project's issue-tracker config, triage-label mapping, ticket brief, and
handoff-comment shape from `docs/agents/`. Then run the tracker config's
**Pickup operations** once:

1. Query the frontier: tickets in the agent-ready triage role, unclaimed, not
   blocked, oldest first. If it is empty, report "no work" and stop.
2. Claim the first one exactly as the config says, then re-read it to confirm the
   claim held. If another session won, take the next.
3. Work the ticket from its brief. Verify against the real artifact using the
   brief's Verify section. Commit on a branch named after the ticket.
4. Post a handoff comment at each checkpoint. On a question only a human can
   answer, post a blocked comment with options and a default, release the claim,
   and stop. On completion, open the PR, post a done comment, move the ticket to
   review, and stop.
5. Never relax the acceptance criteria to finish. Never take a second ticket in
   the same run.

Report: the ticket taken, the final status, and the PR or the open question.
