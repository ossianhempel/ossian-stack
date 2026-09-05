# Hq Bootstrap

Read for bootstrapping HQ or reorienting from the durable ledger. Follow the scope and safety contract in the skill entry point.

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
3. Probe delegation surfaces per `delegation.md` and record the level
   available in this runtime, along with the check-in mechanism HQ will use
   for its heartbeat. Record HQ's exact task/thread id or available messaging
   address and the cross-thread report channel. On GitHub Copilot, also record
   HQ's current checkout path and branch and apply the Copilot boundary before
   any repository work.
4. Record the tracker config at `docs/agents/issue-tracker.md` if present, or
   `none`; read it when a workstream uses tickets. Its absence does not block
   bootstrap, planning, or delegation. A chosen ticket-based workflow needs its
   configuration before tracker operations; request only that missing setup,
   through explicit invocation of `setup-ossian-stack` scoped to the tracker.
   Continue independent work without a machine-wide setup audit.
5. Name and pin this thread per the naming rules.
6. Write the ledger header, then present the operating contract to the user in
   one short paragraph: what HQ does, what it will not do, and how to hand it
   work.
7. If a first task was given, delegate it now.

**Re-orient, bare `/orchestrate-threads` in the HQ thread:**

1. Read the ledger. It is the truth, not your memory of this chat.
2. Run the check-in gate from "Monitoring workstreams" over every open row:
   read each thread's current state where the runtime lets you, fold in any
   report you have not seen (a message the sub-thread sent here, or something
   the user pasted), and verify the artifact each row names.
3. Reconcile the ledger, then report: open workstreams and their state, what
   came back since last time, what is blocked on the human, and what HQ will
   delegate next.

Re-orient reads and reconciles; the only file it writes is the ledger. If the
ledger and the working tree disagree (an edit logged but absent, a branch
missing), report the inconsistency and let the user or the owning thread fix
it. Fixing it here turns a status check into unrequested work.
