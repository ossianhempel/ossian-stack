# Workstream Briefs

Read for briefing and starting an authorized visible workstream. Follow the scope and safety contract in the skill entry point.

## Delegating

Every delegation is a kickoff brief written per `priming.md`. The
brief is the contract; the sub-thread starts with nothing else. It carries the
goal, the done condition, scope boundaries, the project facts the thread cannot
derive, the skills it should invoke and when, and the exact shape of the report
it owes HQ. Copy the user's action scope into it: allowed edits, tracker choice,
working environment, branching rule, delivery actions, and the first action the
thread must not take. Delegation carries existing authorization; it does not add
commit, push, PR, issue, publish, release, or merge permission.

Every initial kickoff and every later assignment or follow-up sent to an existing
workstream carries a return contract. This includes the next item sent to an idle
thread, a correction, resumed work, review fixes, and delivery closeout. Name HQ
exactly and include its task/thread id or the concrete addressing mechanism
available in that runtime. Tell the workstream to report proactively when it:

- finishes;
- is blocked or stuck;
- needs a human decision or input; or
- reaches its authorized stop or delivery boundary.

When cross-thread messaging is available, the workstream sends that structured
report to HQ at the recorded address without waiting to be polled. Otherwise it
posts the same report as its final workstream message so HQ's heartbeat can read
it. Routine chatter is not required, and an unchanged blocker is not reported
again. A later assignment repeats the compact return contract because the thread
may have crossed sessions or lost earlier context.

Before delegating, decide what kind of work it is and route it. The test is
whether the design is already decided, not how large the diff will be:

- A question, research goal, or unsettled design: a plan thread. Give it the
  question, constraints, and expected answer or planning artifact directly.
  Use `grilling` or `prototype` when useful to settle a decision. A spec file
  or ticket is not required; return the findings to HQ and brief implementation
  once the needed decisions are settled.
- Implementation with an agreed outcome and scope: a build thread. Decisions
  accepted in conversation suffice; a spec or ready ticket can supply them too. On
  Claude Code, also point it at `codex-first` so the thread routes typing to
  Codex. A brief for a build thread carries decisions; a brief for a plan
  thread carries the question and the constraints, and leaves the decisions to
  the thread.
- A PR that already exists and needs status or readiness work: `babysit`, in the
  thread that owns the PR. Use its `check` mode for a read-only status request.
- A bug nobody understands yet: `diagnosing-bugs`, and the report is the
  diagnosis, not a fix.

### Start and delivery routes

Normally, the first content line of every visible workstream prompt is the
literal command `/ossian-mode`. Because the kickoff prompt is user-visible, that
line explicitly invokes the skill for the brief that follows. It applies the
project's working standards and chooses only the routes needed inside the
inherited scope. Delete the command for research-only work, human-in-the-loop
planning, `prototype` or `grilling` sessions, read-only/status tasks, and work
the user explicitly bounded to local output with no delivery. Those direct
routes keep their own stated goal and stop.

Every implementation or delivery brief states its closeout route even when
delivery is not yet authorized:

- When the inherited action scope authorizes the required commit, push, and PR
  actions, invoke `commit-push-pr` after the implementation and verification are
  complete. Its default completed, non-draft PR flow invokes or resumes
  `babysit` in `drive` mode and carries the same action scope through review and
  CI to merge-ready. It never merges.
- Do not also start `babysit` or a feedback resolver from the brief for that
  default flow. `commit-push-pr` owns the handoff, and `babysit` owns resolver
  invocation. Resume an existing drive instead of creating a second one.
- Preserve narrower outcomes exactly: local diff only, commit only, push only,
  draft PR, stop at PR, read-only status, or another explicit stop. If the next
  delivery action is not authorized, stop with the concrete result and report
  `awaiting delivery`; do not treat the route as permission.
- In a trunk-direct repository, route authorized commit and push through
  `commit-push-pr`; it stops after the push because the project has no PR or
  babysit stage.

An existing PR whose thread starts with status, feedback, or readiness as its
goal routes directly to the matching `babysit` mode. That is existing-PR
ownership, not a second closeout loop.

Choose tracker-dependent skills only for a workstream using that workflow:
`wayfinder` for large exploratory work managed through tickets, `to-spec` for a
published tracker spec, `to-tickets` for ticket decomposition, and `triage` for an
assigned tracker inbox. Preserve their configuration requirements and explicit
invocation restrictions. They are not a mandatory chain for planning or building,
and naming them in a brief grants no authority to publish or create issues.

Outside GitHub Copilot, trivial edits under about twenty lines with one obvious
change are cheaper to do here than to brief. Do them, note them in the ledger,
move on. Copilot HQ delegates those edits too; its own ledger reconciliation
remains coordination, with delivery handled in the separate worktree session.

After spawning, add or update the ledger row in the same turn, with the time
HQ expects to hear back, and arm the heartbeat if no row was open before. A
delegation that is not in the ledger did not happen as far as the next
`/orchestrate-threads` is concerned.
