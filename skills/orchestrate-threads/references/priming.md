# Priming a sub-thread

A sub-thread starts with nothing: not this chat, not the ledger, not the user's
habits. The kickoff brief is everything it will know. Write it as a work order,
in the brief's voice, so it can be pasted verbatim as the first message of a new
thread.

## Template

```markdown
/ossian-mode

You are the `<Project> · <workstream>` thread. Your HQ is the thread
`<project emoji> <Project>`; it coordinates, you own the work below. Report to HQ.

## HQ return address
- Name: `<exact HQ task/thread name>`
- Address: `<exact task/thread/session id, messaging target, or available addressing mechanism>`
- Channel: <cross-thread message tool/capability | final workstream message>

## Goal
<one paragraph: what done looks like, in behavior, not steps>

## Scope
- In: <bullets>
- Out: <bullets — what you must not touch or gold-plate>

## Facts you cannot derive from the repo
<decisions already made, links to spec/tickets/ADRs, constraints, branch.
For a plan thread: the question to settle and the constraints, not the answer>

## Repository and action scope
- Working location: <exact repo/worktree or not applicable>
- Branching rule: <exact project rule, current branch, and target branch>
- Authorized now: <edit/test/commit/push/open or update PR/fix review feedback/etc.>
- Stop before: <first action not authorized, including merge>
- Delivery result: <local artifact | commit | remote branch | draft PR | PR | merge-ready>

## Tracking
- Choice: <untracked | exact tracker and workflow>
- Owned tickets: <links or none>
- Authorized tracker actions: <read/status/comment/create or none>
For untracked work, report findings and artifact links to HQ and create no issues.
For tracked work, follow the project's concise handoff-comment policy. Tracker
availability and delegation do not authorize writes or issue creation.

## How to work here
1. Read the project's active instructions already in your context, and run the
   docs list if the project has one, before touching code.
2. Work only in the location and branch named above. Preserve the user's scope
   and stop boundary.
3. Invoke these skills at these points:
   <the routed list below, trimmed to what this thread will actually need>
   Skills marked "user types" cannot be invoked by you. When you reach that
   point, stop and ask the person in this thread to type the slash command.
4. Never create another thread. If the work needs one, say so in your report.
5. Report proactively to the HQ address above when you finish, become blocked or
   stuck, need a human decision or input, or reach the authorized stop or delivery
   boundary. Use the named cross-thread channel when available. Otherwise make
   the structured report below your final workstream message so HQ's heartbeat
   can read it. Do not send routine chatter or repeat an unchanged blocker.
   Expect a first report by <time>. Anything the person in this thread tells you
   after this brief overrides it.

## Report
At any report trigger above, send this structure to the exact HQ address without
waiting for HQ to ask:
- Workstream: `<Project> · <workstream>`
- State: done | blocked | stuck | needs human | at authorized stop
- Artifact: <PR, commit, doc link>
- Delivery: <remaining commit/push/merge step, or evidence it reached its destination>
- What changed, in five lines or fewer
- What HQ must decide or the user must do, if anything
- Continuation: <complete | ask the user to type /handoff so this thread can continue>
If cross-thread messaging is unavailable, make this exact report the final message
in the workstream task. Do not add a later status or handoff message.
```

## Skill routing

For a repository workstream delegated by GitHub Copilot HQ, put the verified
child session identity and separate worktree path in the brief, alongside HQ's
checkout path as a do-not-mutate boundary. Carry existing scope and delivery
permissions explicitly. If transferring dirty work or ledger changes, identify
the scoped diff/snapshot and require receipt before applying it in the child's
worktree; preserve HQ's files. Never direct a child to switch, commit, push, or
create a PR from HQ's checkout. This constraint is Copilot-only.

Tell the sub-thread which plugin skills to invoke and when. It has the plugin
installed but no reason to reach for the right one unprompted. Include only the
lines that apply to the thread's kind.

Fill the HQ return address with real values before sending the brief. Prefer the
stable task/thread id accepted by the runtime's messaging tool and include the HQ
name for humans. If there is no cross-thread message capability, name the exact
HQ thread and record `final workstream message` as the channel. Never leave an id
placeholder in a delivered brief.

Keep `/ossian-mode` as the literal first content line of a normal visible
workstream prompt. The kickoff prompt is user-visible, so this command explicitly
invokes the skill for the brief below it; the child does not ask the user to type
it again. Delete the line for research-only work, human-in-the-loop planning,
`prototype` or `grilling`, read-only/status work, and explicitly
local-only/no-delivery work. Do not replace it with a prose suggestion.

Some skills are user-invoke-only: their SKILL.md sets disable-model-invocation
and the agent's skill tool refuses them. In this list they are marked
**(user types)**, and the brief must phrase them as a prompt to the person in
the thread ("ask the user to type /wayfinder"), never as an agent step. The
rest the agent invokes itself.

**Plan threads**

- Give research and planning a direct brief: the question, constraints, evidence
  needed, and expected report or document. No ticket, published spec, or setup
  is required. A settled outcome can become a direct build brief.
- `grilling` when a decision needs discussion, or `grill-me` / `grill-with-docs`
  (user types) when the plan should leave ADRs and glossary entries behind.
- `domain-modeling` when the vocabulary is unsettled.
- `prototype` when a design question is cheaper to answer with throwaway code.

**Chosen ticket workflows only**

- `wayfinder` (user types) for large exploratory work managed through tickets;
  `to-spec` (user types) for a published tracker spec; `to-tickets` (user types)
  for decomposition into tickets. Select the needed skill, not an automatic chain.
- Keep each skill's tracker prerequisites. If configuration is missing, request
  tracker-only setup for that chosen workflow and continue independent research
  or planning. Do not route ordinary work through a full installation audit.

**Build threads**

- After implementation and verification, invoke `commit-push-pr` only through
  the authorized delivery boundary recorded above. If commit, push, or PR work
  is not authorized, stop before it and report `awaiting delivery` with the
  verified local artifact.
- For the default completed, non-draft PR flow, `commit-push-pr` owns the handoff
  to `babysit` drive. Do not add separate `babysit` or `resolve-pr-feedback`
  steps: `babysit` owns resolver invocation and resumes its watcher afterward.
- Preserve explicit local-only, commit-only, push-only, draft, stop-at-PR, and
  other narrow outcomes. In a trunk-direct repo, `commit-push-pr` ends after the
  authorized commit and push.
- `codex-first` on Claude Code sessions, so typing routes to Codex and the
  thread specs, reviews, and verifies.
- `refactoring` for shape changes to working code; `simplify-code` after it
  works; `principle-subtract-before-you-add` (user types) before an addition.
- `autoreview` before every commit that will become a PR.
- The project's own verification skill, if the repo has one, to prove the
  change in the real app by driving the feature the change touched. If there
  is none, say so in the report rather than generating one: `close-the-loop`
  (user types) is a one-time generator HQ has run once per repo, not a
  build-thread step. `principle-prove-it-works` (user types) before declaring
  done.
- For a thread whose starting artifact is an existing PR, route status or
  readiness work directly to the matching `babysit` mode. This is separate from
  the default build closeout above; do not start a second drive.
- `resolving-merge-conflicts` when a rebase stalls.

**Diagnose threads**

- `diagnosing-bugs` as the whole job; the report is the diagnosis and a
  red-capable repro, and HQ decides whether to open a build thread.
- `how` and `why` to understand the code first.

**Every thread**

- On every initial kickoff and every later assignment or follow-up, retain the
  exact HQ return address and proactively report the four trigger states. Use
  cross-thread messaging when it exists; otherwise make the structured report
  the final workstream message. Skip routine updates and unchanged blocker
  repeats.
- Treat the brief's repository, action, tracker, and stop fields as the complete
  inherited authority. A named route does not grant an action missing there.
- Follow the brief's tracking choice. For untracked work, send the report and
  evidence to HQ without creating issues. For an owned ticket, keep status current
  within the granted permissions. Comment only on meaningful progress, a new or
  changed blocker, a decision needed, or completion, in a few sentences with
  evidence links and no empty sections. Do not repeat unchanged blockers or copy
  HQ/agent coordination into the tracker. Preserve necessary claim/release/resume
  records; keep durable decisions in the ticket/spec and link detailed evidence.
  Report a blocked tracker update honestly;
  it does not erase completed work or prevent reporting it to HQ.
- `handoff` (user types) at the end of every session in the thread, so the next
  session continues instead of restarting. When the structured report must be
  the final message, put the request to type `/handoff` in its Continuation line;
  do not send a second message afterward.
- `one-password` for any secret, never plaintext.
- Platform skills when the work touches them: `convex-cli`, `clerk-cli`,
  `revenuecat-api` (user types), `coolify`, `hetzner-vm`, `post-queue-cli`, and
  the iOS set (`release-ios-app`, `asc-release`, `asc-metadata`,
  `asc-version-guard`).
- `triage` (user types) only in a thread HQ has explicitly given the tracker's
  inbox.
