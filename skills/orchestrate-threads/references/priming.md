# Priming a sub-thread

A sub-thread starts with nothing: not this chat, not the ledger, not the user's
habits. The kickoff brief is everything it will know. Write it as a work order,
in the brief's voice, so it can be pasted verbatim as the first message of a new
thread.

## Template

```markdown
You are the `<Project> · <workstream>` thread. Your HQ is the thread
`<project emoji> <Project>`; it coordinates, you own the work below. Report to HQ.

## Goal
<one paragraph: what done looks like, in behavior, not steps>

## Scope
- In: <bullets>
- Out: <bullets — what you must not touch or gold-plate>

## Facts you cannot derive from the repo
<decisions already made, links to spec/tickets/ADRs, constraints, branch.
For a plan thread: the question to settle and the constraints, not the answer>

## Tracking
<Untracked: report findings and artifact links to HQ; create no issues.
Or tracked: owned ticket links, selected workflow, and permitted status/comment
updates. Include issue creation only when authorized. Tracker availability and
delegation do not authorize it. Preserve the user's explicit tracking choice.>

## How to work here
1. Read the project's active instructions already in your context, and run the
   docs list if the project has one, before touching code.
2. Use `<agreed working environment and branch, if applicable>`. Preserve the
   user's scope and permissions; do not merge, release, or push to
   `<protected branch>` without the required authorization.
3. Invoke these skills at these points:
   <the routed list below, trimmed to what this thread will actually need>
   Skills marked "user types" cannot be invoked by you. When you reach that
   point, stop and ask the person in this thread to type the slash command.
4. Never create another thread. If the work needs one, say so in your report.

## Report
When done, or when blocked, end with a message to HQ shaped as:
- Workstream: `<Project> · <workstream>`
- State: awaiting delivery | done | blocked | needs decision
- Artifact: <PR, commit, doc link>
- Delivery: <remaining commit/push/merge step, or evidence it reached its destination>
- What changed, in five lines or fewer
- What HQ must decide or the user must do, if anything
Make this the last message of the session so it can be copied to HQ as is.
Then ask the user to type /handoff (`handoff` is user-invoked) so the next
session in this thread can continue.
```

## Skill routing

Tell the sub-thread which plugin skills to invoke and when. It has the plugin
installed but no reason to reach for the right one unprompted. Include only the
lines that apply to the thread's kind.

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
- `babysit` once the PR exists, in this same thread, until merge-ready. Never
  merge.
- `resolve-pr-feedback` when a human has left review comments.
- `resolving-merge-conflicts` when a rebase stalls.

**Diagnose threads**

- `diagnosing-bugs` as the whole job; the report is the diagnosis and a
  red-capable repro, and HQ decides whether to open a build thread.
- `how` and `why` to understand the code first.

**Every thread**

- Follow the brief's tracking choice. For untracked work, send the report and
  evidence to HQ without creating issues. For an owned ticket, keep status current
  at start and stop and record each HQ report with artifact links and remaining
  work, within the granted permissions. Report a blocked tracker update honestly;
  it does not erase completed work or prevent reporting it to HQ.
- `handoff` (user types) at the end of every session in the thread, so the next
  session continues instead of restarting.
- `one-password` for any secret, never plaintext.
- Platform skills when the work touches them: `convex-cli`, `clerk-cli`,
  `revenuecat-api` (user types), `coolify`, `hetzner-vm`, `post-queue-cli`, and
  the iOS set (`release-ios-app`, `asc-release`, `asc-metadata`,
  `asc-version-guard`).
- `triage` (user types) only in a thread HQ has explicitly given the tracker's
  inbox.
