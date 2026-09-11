# Priming an execution owner

An owner starts without HQ chat or ledger context. Send a complete work order.

## Template

```markdown
/ossian-mode

You own queue item `<Q-ID>` in workstream `<Project> · <workstream>`. HQ
coordinates the project; report only to HQ.

## HQ return address
- Name: `<exact HQ task name>`
- Address: `<exact task/session id or addressing mechanism>`
- Channel: <cross-task message | subagent result | final owner message>

## Outcome and proof
- Done: <observable result>
- Behavior or claim: <what must be proved>
- Real surface and starting state: <browser, simulator, API, CLI, logs, or N/A>
- Evidence: <screenshots/recording/diff | logs/commands/API results | other>

## Scope and dependencies
- In: <bounded work>
- Out: <excluded work>
- Depends on: <queue IDs, decisions, artifacts, or none>
- Project facts: <decisions and links the owner cannot derive>

## Repository and authority
- Working location: <exact repo/worktree or N/A>
- Branch and target: <exact project rule>
- Authorized now: <actions>
- Stop before: <first unauthorized action>
- Delivery result: <local artifact | commit | remote branch | draft PR | PR | merge-ready>
- Tracking: <untracked | exact tracker and owned items>
- Tracker actions: <authorized actions or none>

## Working rules
1. Read the project's active instructions and docs index when available.
2. Preserve the location, scope, authority, and stop boundary above.
3. Invoke only the routed skills below. If an explicit-only skill becomes
   necessary but was not invoked in this user-visible assignment, report that to
   HQ; do not ask the user to enter this task.
4. Never create another owner. Ask HQ through the report when separation is
   needed.
5. Report proactively at completion, blockage or repeated failure, human-input
   need, or the authorized stop boundary. Stay quiet for routine progress and an
   unchanged blocker. Expect a first report by <time>.

## Report
- Queue item: `<Q-ID>`
- Workstream: `<Project> · <workstream>`
- State: done | blocked | stuck | needs human | at authorized stop
- Artifact: <PR, commit, document, or path>
- Delivery: <remaining step or proof it reached the destination>
- Evidence: <required results and links, or `unverified: <reason>`>
- What changed: <five lines or fewer>
- HQ decision needed: <decision, evidence, recommendation, or none>
- Continuation: <complete | exact next action HQ should send>
```

Delete `/ossian-mode` for bounded subagents, research-only work,
human-in-the-loop planning or prototypes, read-only status, and explicit
local-only work. Keep it as the literal first content line for normal durable
implementation tasks; the kickoff itself is user-visible and explicitly invokes
the skill.

## Routing

Include only skills needed for this owner:

- **Plan:** `grilling`, `domain-modeling`, or `prototype` when the question needs
  them. If an explicit-only workflow is required later, return the need to HQ so
  HQ can send the invocation.
- **Build:** `commit-push-pr` only through recorded authority. Its normal PR flow
  owns the single `babysit-pr` handoff. Use `refactoring`, `simplify-code`,
  `autoreview`, the project's verification skill, and platform skills only when
  applicable.
- **Diagnose:** `diagnosing-bugs` as the job; use `how` or `why` for code
  understanding.
- **Existing PR:** route directly to the applicable `babysit-pr` mode.
- **All owners:** use `one-password` for secrets. Follow the selected tracker
  policy and report concise evidence links. A tracker record is never delivery
  proof.

For GitHub Copilot repository work, include both HQ's do-not-mutate checkout and
the owner's verified separate session and worktree. For a resumed session that
needs `handoff` or another explicit-only action, the owner reports the need and HQ
sends the explicit user-visible invocation through the recorded channel.
