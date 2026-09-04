# Priming a sub-thread

A sub-thread starts with nothing: not this chat, not the ledger, not the user's
habits. The kickoff brief is everything it will know. Write it as a work order,
in the brief's voice, so it can be pasted verbatim as the first message of a new
thread.

## Template

```markdown
You are the `<Project> · <workstream>` thread. Your HQ is the thread
`<project emoji> <Project>`; it decides, you build. Report to it, not to the user.

## Goal
<one paragraph: what done looks like, in behavior, not steps>

## Scope
- In: <bullets>
- Out: <bullets — what you must not touch or gold-plate>

## Facts you cannot derive from the repo
<decisions already made, links to spec/tickets/ADRs, constraints, branch.
For a plan thread: the question to settle and the constraints, not the answer>

## How to work here
1. Read the project's active instructions already in your context, and run the
   docs list if the project has one, before touching code.
2. Work in this thread's worktree on branch `<branch>`. Do not merge, release,
   or push to `<protected branch>`; HQ hands those to the user.
3. Invoke these skills at these points:
   <the routed list below, trimmed to what this thread will actually need>
   Skills marked "user types" cannot be invoked by you. When you reach that
   point, stop and ask the person in this thread to type the slash command.
4. Never create another thread. If the work needs one, say so in your report.

## Report
When done, or when blocked, end with a message to HQ shaped as:
- Workstream: `<Project> · <workstream>`
- State: done | blocked | needs decision
- Artifact: <PR, commit, doc link>
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

- `wayfinder` (user types) when the work is too big for one session and the
  way is foggy. The thread's output is a resolved map, not code.
- `to-spec` (user types) to turn a settled discussion into a published spec.
- `to-tickets` (user types) to break a spec into tracer-bullet tickets on the
  tracker. HQ then opens build threads per ticket cluster.
- `grilling` before committing to a plan, or `grill-me` / `grill-with-docs`
  (user types) when the plan should leave ADRs and glossary entries behind.
- `domain-modeling` when the vocabulary is unsettled.
- `prototype` when a design question is cheaper to answer with throwaway code.

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

- Keep the ticket you own on the tracker current: move its status when you
  start and when you stop, and leave one comment per report you send HQ saying
  what landed, the link, and what is still open. HQ reads the tracker for
  detail and your report for the headline; a report that claims something the
  ticket does not show gets sent back.
- `handoff` (user types) at the end of every session in the thread, so the next
  session continues instead of restarting.
- `one-password` for any secret, never plaintext.
- Platform skills when the work touches them: `convex-cli`, `clerk-cli`,
  `revenuecat-api` (user types), `coolify`, `hetzner-vm`, `post-queue-cli`, and
  the iOS set (`release-ios-app`, `asc-release`, `asc-metadata`,
  `asc-version-guard`).
- `triage` (user types) only in a thread HQ has explicitly given the tracker's
  inbox.
