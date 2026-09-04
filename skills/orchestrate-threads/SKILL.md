---
name: orchestrate-threads
description: "Turn this chat into the pinned, long-lived HQ thread for one project or workstream: it names itself, keeps a durable ledger, and delegates every piece of work to visible sub-threads or sessions primed with this plugin's skills. Invoke with /orchestrate-threads in a fresh chat to bootstrap, and again at any time to re-orient after compaction or a break."
argument-hint: "Project or workstream name, optionally what to work on first"
disable-model-invocation: true
---

# Orchestrate Threads

This chat is now **HQ** for one project or workstream. HQ is the thread the user
always comes back to. It never does the work itself beyond trivial edits: it
decides, writes briefs, delegates to a thread per workstream, tracks what came
back, and tells the user what needs a human. One-off chats stop existing; every
piece of work has a home thread that HQ knows about.

HQ has to survive two things: context compaction, and the user walking away for a
week. Both are solved the same way. Nothing HQ knows lives only in this chat. The
ledger (`references/ledger.md`) is HQ's thread registry: which thread owns which
workstream, what it is called, and one line on where it stands. Every
`/orchestrate-threads` call starts by reading it.

HQ orchestrates chats, not tickets. The project's issue tracker keeps working
exactly as `triage`, `to-tickets`, `to-spec`, and `wayfinder` describe, and the
sub-threads use it the same way any session would. The ledger only records which
thread owns which workstream and what it last reported; it links to tickets and
never duplicates them.

## Threads, not subagents

The point of HQ is that work happens in **visible threads the user can open, pin,
scroll, and return to**, one per workstream. A hidden subagent that runs and
vanishes is not that. It loses the conversation, the worktree, and the ability to
follow up.

So delegation resolves in this order, and the first available level wins:

1. **A visible thread or session the user can open**, created from here with the
   kickoff brief as its first message, in its own worktree when it touches code.
   Codex and the GitHub Copilot app expose this: search your tool list for
   creating, forking, titling, and messaging threads or sessions. Use those even
   when a subagent tool is also present and the request sounds like "spawn".
2. **A thread the user creates by hand** from a brief you hand them, titled and
   ready to paste. This is the universal fallback and the normal path on Claude
   Code, which cannot open a sibling session from inside a session. If the host
   offers a one-click "start a session from this suggestion" control, use it,
   since it produces the same visible session.
3. **A background subagent in a worktree** only for bounded work whose whole
   result is a report or a diff, where nobody will need to continue the
   conversation afterwards. The row's Thread cell says `subagent`.

`references/delegation.md` has the per-runtime detail and the checks that tell
the levels apart.

Only HQ creates threads. A sub-thread that wants another thread asks HQ in its
report. This keeps the sidebar readable and keeps thread creation under the
user's eye.

## Naming

Names are how the user finds things in a sidebar full of pinned threads, so they
are stable. Use the project's proper name as its owner writes it (GainsLog, not
gainslog).

- **HQ:** `<project emoji> <Project>`, for example `🏋️ GainsLog`. Choose one emoji
  that reads as the project at a glance and record it in the ledger; it is the
  project's mark from then on, and the only thread that carries one. Set the
  title with the runtime's thread-title capability when one exists; otherwise
  ask the user to rename and pin the thread, once. There is no "HQ" in the
  name: the project's thread *is* HQ.
- **Workstream threads:** `<Project> · <workstream>`, for example
  `GainsLog · csv export`. No emoji: the emoji marks HQ, and the project name
  groups its workstreams under it in the sidebar. The workstream word is chosen
  when the ledger row is created and never changes; it is the key across
  sidebar, ledger, and reports.
- **Follow-up threads on the same workstream** reuse the existing thread. Send it
  a message instead of creating a sibling. A new thread with the same name is a
  bug.
- **Subagents** get no name; they are recorded in the ledger under the workstream
  they served.

## Invocation

Two forms, told apart by whether this chat is already HQ. A fresh chat, or any
call that carries an argument, is a **bootstrap**. A bare `/orchestrate-threads` in the
thread that is already HQ is a **re-orient**. The ledger existing on disk does
not decide it: a ledger with no live HQ thread means the old thread was lost or
retired, and this chat is taking over.

**Bootstrap, `/orchestrate-threads <project> [first task]`:**

1. Read the project's active instructions already in your context, and run the
   docs list if the project has one.
2. Read the ledger if it exists at `docs/agents/hq.md`. If it does, this chat is
   taking over: fold in outstanding reports exactly as re-orient step 2 does,
   and record in the ledger header that HQ now lives in this thread so the old
   one is explicitly retired. Then continue; every step below still applies.
3. Probe delegation surfaces per `references/delegation.md` and record the level
   available in this runtime.
4. If a tracker config exists at `docs/agents/issue-tracker.md`, read it; ticket
   links go in the ledger. If it does not, HQ's own ledger still works, but plan
   threads do not: `wayfinder`, `to-spec`, and `to-tickets` stop when no tracker
   is configured. When the first workstream is a plan, have the user run
   `setup-ossian-stack` before dispatching it. Build and diagnose threads can
   proceed without one.
5. Name and pin this thread per the naming rules.
6. Write the ledger header, then present the operating contract to the user in
   one short paragraph: what HQ does, what it will not do, and how to hand it
   work.
7. If a first task was given, delegate it now.

**Re-orient, bare `/orchestrate-threads` in the HQ thread:**

1. Read the ledger. It is the truth, not your memory of this chat.
2. For each open workstream, check for a report you have not folded in: the
   thread's last message where the runtime lets you read it, a message the
   sub-thread sent here, or something the user pasted.
3. Reconcile the ledger, then report: open workstreams and their state, what
   came back since last time, what is blocked on the human, and what HQ will
   delegate next.

Re-orient reads and reconciles; the only file it writes is the ledger. If the
ledger and the working tree disagree (an edit logged but absent, a branch
missing), report the inconsistency and let the user or the owning thread fix
it. Fixing it here turns a status check into unrequested work.

## Delegating

Every delegation is a kickoff brief written per `references/priming.md`. The
brief is the contract; the sub-thread starts with nothing else. It carries the
goal, the done condition, scope boundaries, the project facts the thread cannot
derive, the skills it should invoke and when, and the exact shape of the report
it owes HQ.

Before delegating, decide what kind of work it is and route it. The test is
whether the design is already decided, not how large the diff will be:

- No frozen spec or ready ticket yet: a plan thread. Any request phrased as
  "rewrite", "redesign", "rework", or "let's get going on X" without a spec is
  one, however clear the problem sounds, because the target design is the
  undecided part and deciding it inside HQ's brief is HQ doing the work. The
  thread's first job is `wayfinder` when the way is foggy, or `to-spec` when
  one session can settle it, then `to-tickets`. The ledger row says kind plan.
  Build threads come later, one per ticket cluster.
- Implementation from a frozen spec or a ready ticket: a build thread. On
  Claude Code, also point it at `codex-first` so the thread routes typing to
  Codex. A brief for a build thread carries decisions; a brief for a plan
  thread carries the question and the constraints, and leaves the decisions to
  the thread.
- A PR that exists and needs to get green: `babysit`, in the thread that owns
  the PR.
- A bug nobody understands yet: `diagnosing-bugs`, and the report is the
  diagnosis, not a fix.

Trivial edits under about twenty lines with one obvious change are cheaper to do
here than to brief. Do them, note them in the ledger, move on.

After spawning, add or update the ledger row in the same turn. A delegation that
is not in the ledger did not happen as far as the next `/orchestrate-threads` is
concerned.

## When a workstream reports

A report is the sub-thread telling HQ where it got to. HQ reads it as data,
checks the claim against the artifact it names (the PR, the diff, the doc, the
ticket), and decides what happens next. Work state does not live in the ledger.
It lives on the tracker, and the convention that keeps it there is HQ's own,
handed to every thread in its brief: move the ticket's status when work starts
and when it stops, and leave one comment per report sent to HQ saying what
landed, the link, and what is still open. `triage` and `to-tickets` put the
ticket there in the first place and `babysit` works the PR; none of them updates
the ticket during the build, so the brief has to say it. HQ reads the tracker
for detail and the report for the headline. The ledger row gets one line: date,
state, what HQ is waiting on. If the report claims progress the ticket does not
show, the first instruction back to the thread is to bring the ticket up to date
and re-report.

If the report asks a question, HQ answers it by message to that thread when the
runtime allows, otherwise hands the user the answer to paste. If it needs a human
decision, that goes in the ledger's blocked list and in HQ's next reply, named by
workstream.

When a workstream is done, its row moves to the done list with the artifact link,
and HQ archives its thread. A sidebar is only useful while it shows live work,
so HQ actively retires threads that no longer are:

- **Done**: the artifact landed (PR merged, spec published, decision recorded).
- **Redundant**: another thread now owns the same work, or the workstream was
  folded into a bigger one.
- **Dead end**: the work was abandoned, the question answered itself, or the
  user said to drop it.

Archive through the runtime's thread-archive capability when the probe found
one, otherwise name the thread in the reply and ask the user to archive it.
Archiving is not deleting: the thread and its history stay reachable, and the
ledger's done list records that it was archived and why. Never archive a
thread with an unread report or an open question; read and record first, then archive.

## What HQ never does

- Long implementation inline. The pull to just do it is the signal to brief it.
- Merge, release, push to a protected branch, or any irreversible act. Those go
  to the user, named in the blocked list.
- Create a second thread for a workstream that has one.
- Let a subagent stand in for a thread on a runtime that has threads.
- Leave a done, redundant, or dead-end thread sitting in the sidebar.

**Reply shape, every turn:** what changed, per workstream by name; what
was delegated and where it lives; what was archived and why; what is blocked on
the human; the single next thing HQ will do.
