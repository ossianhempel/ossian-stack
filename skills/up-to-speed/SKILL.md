---
name: up-to-speed
description: Catch the user up on a thread they lost track of — what was done, where it stands now, and what is left — checked against live repo and PR state. Use when they ask to be caught up, ask where things stand, or return to a long or summarized thread. Not for continuing the work.
---

# Up to speed

The user has come back to a thread they no longer remember. The transcript may
be long, compacted into a summary, or a different thread they point you at.
Give them back the picture in a minute of reading: what this was about, what
got done, where it actually stands now, and what still needs them.

This is a report. Do not resume the work, fix anything, commit, or push while
catching them up. Offer the next step at the end and wait.

## Rebuild the picture

1. **Goal.** What the user asked for at the start, and how it changed along the
   way. Later instructions override earlier ones.
2. **What happened.** The decisions made and the work done, as outcomes, not as
   a replay of every step. Drop dead ends unless one explains a current choice.
3. **Live state.** The transcript says what was intended; the repo says what is
   true. Check current state directly: uncommitted changes, branch, commits not
   pushed, open or merged PRs and their checks, deploys or releases if the
   thread touched them. When the transcript and live state disagree, live state
   wins, and the disagreement itself is worth telling the user. If you cannot
   reach a source (no remote access, no PR tool), say what you could not check.
4. **What is left.** Anything promised but not done, failing checks or tests,
   review comments not addressed, questions the user never answered, things the
   agent flagged as unverified or broken, and temporary work (stashes, scratch
   branches, debug code, running servers) that needs cleaning up.

Stay inside what the thread and the live state show. Do not guess at work that
might have happened elsewhere; say it is unknown.

## Tell it

Write like one person catching a colleague up, in plain words. No jargon the
user did not use themselves, no tool names or command output unless they need
to act on it. Short sentences. Name files, branches, and PRs only where they
help the user find something.

Use this shape, dropping any section with nothing in it:

- **The short version:** two or three sentences — what this thread was for and
  where it stands now.
- **Done:** the outcomes, a few bullets.
- **State right now:** saved, committed, pushed, merged, or released — say
  exactly how far each piece got. Lead with anything surprising, such as
  changes that were never committed or a PR that is still open.
- **Needs you:** open questions and decisions waiting on the user.
- **Still to do or fix:** leftovers, failures, and cleanup, most important first.
- **Next step:** one suggested move, as an offer.

Done when the user can say what happened, what state it is in, and what to do
next without scrolling back.
