---
name: up-to-speed
description: "Catch the user up on a thread: progress since their last message, current state, and decisions needing them, with context and recommendations. Use for catch-up requests, where things stand, what changed while away, or what needs their attention. A report, not authorization for new work."
---

# Up to speed

Give the user the picture in a minute of reading: what changed, where the work
actually stands, and what needs their attention. Include enough background for
them to make a pending decision without reading the thread again.

The catch-up itself is read-only. It does not authorize fixes, cleanup, tests,
commits, pushes, merges, or releases. For a recap-only request in an idle thread,
report and stop. Honor separately requested follow-on work under its own scope.
A status request during active work does not cancel or pause its existing
authorization: give the update, then continue unless the user asks to stop or wait.

## Set the window

Use the current thread unless the user names another thread or set of projects.
Read only the relevant history and known linked work; do not launch workers or
turn the recap into a search across all projects.

- **Since my last message / while I was away:** start after the user's previous
  message before this catch-up request. Honor an explicit date, message, or other
  boundary instead when supplied. Automated wakeups and tool events are not user
  messages. Give only the earlier background needed to understand the changes.
- **Lost track / get me up to speed / where are we:** briefly restore the goal,
  then summarize outcomes and current state rather than replaying the thread.
- If compaction or unavailable history hides the requested boundary, say which
  period is visible and give a useful recap of that evidence. Do not invent what
  happened since an unknown message or block the report just to establish a date.

An older unresolved decision or blocker still belongs in the report when it
affects what happens next. Label it as still open rather than new progress.

## Rebuild the picture

1. **Goal.** What the user asked for at the start, and how it changed along the
   way. Later instructions override earlier ones.
2. **What happened.** The decisions made and the work done, as outcomes, not as
   a replay of every step. Drop dead ends unless one explains a current choice.
3. **Live state.** The transcript says what was intended; the repo says what is
   true. Use proportionate read-only checks of relevant state: uncommitted
   changes, branch, commits not pushed, PRs and their checks, deploys or releases
   if the thread touched them. Use the corresponding artifact or task state for
   non-code work; a recap need not involve a repository. When the transcript and
   live state disagree, current evidence wins. If a source is unavailable, state
   the last confirmed milestone, what was still unfinished then, and what cannot
   be verified now. Do not rerun tests or builds to produce a recap, or turn a
   local result into a claim of publication.
4. **What is left.** Anything promised but not done, failing checks or tests,
   review comments not addressed, questions the user never answered, things the
   agent flagged as unverified or broken, and temporary work (stashes, scratch
   branches, debug code, running servers) that needs cleaning up.

Stay inside what the thread and the live state show. Do not guess at work that
might have happened elsewhere; say it is unknown.

## Make decisions answerable

Separate work the agent can already do from decisions, access, or actions that
really require the user. Do not hand routine investigation or authorized fixes
back to them. Check later messages and current evidence before repeating an old
question; an answered or superseded question is no longer pending.

For each item that needs the user, give a compact decision brief:

- **The call:** the exact decision or action needed, and what it unblocks.
- **Context:** the relevant goal, what was learned, and why this remains open.
- **Choices and recommendation:** viable options and their material tradeoffs;
  recommend one with a reason grounded in the evidence. If evidence cannot
  support a choice, name the missing fact and the next way to establish it.
- **Timing:** a real deadline or consequence of waiting, if known. Do not invent
  urgency or an estimated cost. State the concrete approval boundary when relevant.

An access request needs the exact resource and action, not artificial alternatives.
If nothing requires the user, say so plainly. A recommendation is not a decision
already made, and the recap does not request approval again for authorized work.

## Tell it

Write like one person catching a colleague up, in plain words. No jargon the
user did not use themselves, no tool names or command output unless they need
to act on it. Short sentences. Name files, branches, and PRs only where they
help the user find something.

Use only the parts that help; a small update can be one paragraph:

- **The short version:** two or three sentences — what this thread was for and
  where it stands now.
- **What changed:** outcomes in the requested window, a few bullets. If nothing
  changed, say so instead of presenting older work as new.
- **State right now:** saved, committed, pushed, merged, or released — say
  exactly how far each piece got. Lead with anything surprising, such as
  changes that were never committed or a PR that is still open.
- **Needs you:** the decision briefs above, or an explicit statement that no
  action is needed from the user.
- **Still to do:** agent work, failures, and cleanup, most important first.
- **Next step:** the next useful move and who owns it. A recap-only request in an
  idle thread ends with the suggestion; active or explicitly requested follow-on
  work continues under its existing scope.

Done when the user knows what changed, how far it actually got, and can answer
each pending decision without scrolling back. Keep the report in the thread;
create no extra report file or tracker unless requested.
