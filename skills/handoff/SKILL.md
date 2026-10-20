---
name: handoff
description: Write a compact handoff so a fresh session can continue this work, save it, and copy it to the clipboard.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

# Handoff

Write a note another agent can be given in a fresh session and continue from
without this conversation. If the user passed arguments, they set the next
session's focus.

Finish the current atomic step or back it out, and start nothing new. Do not
commit, push, or open a PR just to hand off unless the user already authorized it.

## Write it

Include only what the next agent cannot read from the repo. Point at specs, plans,
commits, PRs, and files by path or URL instead of copying them. Redact secrets and
personal data.

Open with one line to the next agent: check this note against current Git and PR
state before acting, trust live state where they disagree, and do not redo work
the note records as verified. Then cover, skipping anything empty:

- The goal, the done condition, and any authority or limits the user set.
- Where the work lives: repo, branch or worktree, uncommitted or unpushed
  changes, open PR.
- What is done and the evidence for it; what was tried and ruled out, and why.
- Blockers and open decisions.
- The first concrete next step.

## Save and copy

Write the note to `handoff-<YYYYMMDD-HHMMSS>.md` in the system temp directory
(`$TMPDIR`, else `/tmp`), then copy it in one shell call:

```bash
f="<absolute path of the note>";
if command -v pbcopy >/dev/null; then pbcopy < "$f";
elif command -v clip.exe >/dev/null; then clip.exe < "$f";
elif [ -n "$WAYLAND_DISPLAY" ] && command -v wl-copy >/dev/null; then wl-copy < "$f";
elif command -v xclip >/dev/null; then xclip -selection clipboard < "$f";
elif command -v xsel >/dev/null; then xsel --clipboard --input < "$f";
else exit 3; fi
```

A non-zero exit means nothing was copied, which is normal in a remote or headless
session.

Done when the user has the note's path and either knows it is on their clipboard
or, if the copy failed, has the note printed in one fenced block to copy by hand.
