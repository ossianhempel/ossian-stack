# Handoff comment

Copy this file to the project's `docs/agents/handoff-comment.md` and delete this
introductory paragraph. It governs concise tracker updates and recovery records.
A fresh agent resumes from the ticket/spec, relevant ownership and handoff records,
and linked evidence together, not from the latest comment alone.

---

# Handoff comment

Comment on meaningful progress, a new or changed blocker, a decision needed, or
completion. Read recent comments first: do not repeat an unchanged blocker or
already-recorded result. Do not mirror HQ reports, agent coordination, polls, or
routine checkpoints. A status field can be reconciled without a new comment.

Default to a few sentences: what changed, the evidence link, and any next action
or decision needed. Omit empty sections, unchanged details, and transcript-style
logs. Use the AI disclosure required by the project's triage configuration.
Record accepted technical decisions in the ticket body or linked spec; link
detailed test results, logs, and other evidence instead of copying them here.

For a decision, ask the precise question and give only the context or options
needed to answer it. Do not invent a default decision or deadline. For completion,
summarize the verified acceptance outcome, link the artifact and checks, and say
whether delivery is still pending. Follow the tracker's review/done transitions;
a finished local implementation or open PR is not a delivered change.

Example progress comment (after any required disclosure):

> Custom shopping items now persist after reopening. The focused checks passed
> ([results](<evidence-url>)); [the diff](<diff-url>) is ready for review.

## Ownership and recovery

Keep the short ownership records required by the tracker's claim/release protocol.
They are necessary state changes, even when there is no implementation progress.
Preserve claim-before-assignment ordering, winner selection, and release operations.

- **Claim:** record `Claimed by <runtime>:<session-id>` before setting the owner
  where the tracker requires it. Keep the comment timestamp/order for arbitration.
- **Release or pause:** identify the releasing `<runtime>:<session-id>` and the
  disposition of the claim. For unfinished work, include the recoverable
  branch/head and PR or artifact location, current work state, and first resume
  action; link unchanged context.
  Make unfinished work recoverable under the project's permissions before handoff,
  and state any remaining dirty work and where it lives.
- **Resume:** read the ticket/spec and relevant claim, release, and evidence
  history. Record the new claim as the protocol requires; do not repost the old
  handoff or blocker merely because a different runtime resumed the work.

A new blocker can share one concise comment with its claim-release record. Later
polls with the same blocker and no ownership change add nothing. Evidence and
recovery pointers must be usable from another runtime: repository/commit/PR links,
shared documents, or an explicit recoverable artifact location. A private chat or
Codex-only link may supplement them but cannot be the only handoff context.
