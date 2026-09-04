# Delegation surfaces

The rule in the skill is *visible thread first, hand-made thread second, hidden
subagent last*. This file is how to tell which level a runtime gives you. Tool
names change between builds and are sometimes withheld from a session even when
the runtime has the feature, so probe by capability, record what you found in
the ledger, and re-probe when a later session looks different.

## Probe

Look through the tools available in this session for these capabilities:

| Capability | What it proves |
| --- | --- |
| Create a thread or session, optionally in a worktree, with a first message | Level 1 spawn |
| Send a message to an existing thread or session | Follow-ups without new threads; reports can come back by message |
| Set a thread's title, pin it | HQ can name itself and its threads |
| Archive a thread | HQ can retire done, redundant, and dead-end threads itself; without it, it asks the user each time |
| Spawn a subagent that returns a result to this thread | Level 3 only |

A runtime can have the subagent tool without any of the thread tools. That is the case the
skill exists to catch: a subagent tool present while thread tools are absent
means level 2, not level 3, unless the work is a bounded report.

If the runtime's own instructions or tool descriptions say thread creation needs
an explicit user request, the `/orchestrate` invocation plus the ledger row is
that request; say so in the ledger and in the reply.

## What each runtime looks like today

Recorded so a probe result can be sanity-checked. Verify against the session,
never assume from this table.

- **Codex app.** Has thread creation, forking, titling, pinning, archiving, and
  cross-thread messaging, plus a separate subagent tool. The subagent tool is
  the one the model reaches for on the word "spawn"; do not. New threads appear
  in the sidebar as ordinary user threads. Some builds and remote-started
  threads withhold the thread tools; then fall to level 2.
- **GitHub Copilot app.** Sessions are the unit; each runs in its own worktree
  or cloud sandbox and shows in the sidebar and the My Work view. Where the
  session exposes session creation and messaging, that is level 1. Fleet mode
  and custom agents are hidden subagents: level 3.
- **Claude Code.** Cannot open a sibling session from inside a session. The
  desktop app can list other sessions and message them, and can offer the user
  a one-click chip that starts a new session from a suggestion; that chip is a
  level 2 spawn and the preferred one. Background agents, worktree agents, and
  remote agents are level 3.
- **Anything else.** Level 2 until proven otherwise.

## Level 2, the hand-made thread

Give the user two things, in a fenced block they can copy: the title per the
naming rules, and the kickoff brief. Tell them where to create it (new thread in
the same project, worktree on). The row's `Thread` cell is `pending` until the
user confirms the thread exists, then the exact title.

Reports from a level 2 thread arrive only because the user pastes them. The
brief's Report block is the paste-sized shape; say in the brief that it is the
last message of the session so it is easy to copy. `handoff` is not a report
channel: it writes a continuation document for the next session in that same
thread, and the user runs it.

## Level 3, the subagent

Use a worktree. Give it the same brief. Its result is folded into the ledger
under the workstream it served, with `subagent` in the row's `Thread` cell,
because nobody can return to it later.
