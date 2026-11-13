# Eval cases

Read when a lesson lands on the prose rung. An eval case is a regression test for agent behaviour: it replays a real miss and checks that the reader of the edited prose now gets it right. Prompts and instructions are part of the software, so they get tests too.

## Layout

Cases live in the target project, at its top level:

```
evals/
  README.md          what a case is and how to replay one
  cases/<slug>.md    one miss per file
  results/           last replay output per case (gitignored)
```

If `evals/` does not exist, create it with the first case: the README below, `cases/`, and a `results/` entry in the project's `.gitignore`.

```markdown
# Evals

Regression cases for agent behaviour. Each case in `cases/` is a real miss: a
mistake an agent made that a human caught. A case replays the state where the
miss should have been caught and checks that the agent now catches or avoids it.
Add a case whenever an instruction, standard, or skill is changed to fix a miss;
the case must fail before the change and pass after it. Replay results go to
`results/`, which is not committed.
```

## Case file

```markdown
---
reader: reviewer            # reviewer | author
source: <link to the comment, log, or report that caught it>
base: <sha>                 # the miss commit's parent, or the PR merge base
miss: <sha>                 # the state where it should have been caught
fix: <sha>                  # the commit that fixed it
guards: [CODING_STANDARDS.md]   # the prose files this case tests
task: <author cases only: the request the author was given, as given>
added: <YYYY-MM-DD>
---

## Expected

The defect, stated the way a good reviewer would report it: what, where, and
why it matters. This is the grading key. It is never shown to the agent under test.

## Notes

What happened, and anything a grader needs to judge a near-match.
```

Make sure `base`, `miss`, and `fix` are reachable from the default branch or a ref the remote keeps (fetch `pull/<n>/head` for a PR that was squash-merged), so the case still replays after the branch is deleted.

## Reviewer replay

Tests prose aimed at the reviewer, in practice `CODING_STANDARDS.md`, which `autoreview` reads on every review. Run it from the current checkout so the replay uses the standards as they are now, not as they were at the miss:

1. Build a single commit holding the whole miss, without touching any ref:
   `git commit-tree <miss>^{tree} -p <base> -m "eval replay <slug>"` prints its sha.
2. Run `autoreview`'s helper as that skill documents, with `--mode commit --commit <replay sha> --json-output evals/results/<slug>.json`. Pass nothing about the expected finding: no prompt, no slug, no hint. A replay that is told what to look for proves nothing.
3. Grade (below).

## Author replay

Tests prose aimed at the agent doing the work: the project's agent instructions, a skill, a doc. It reruns the task, so it costs more and varies more than a reviewer replay.

1. `git worktree add --detach <scratch dir> <base>`, then copy the current version of every `guards` file into it, so the run sees the edited prose on the old code.
2. Dispatch a fresh subagent that inherits nothing from this session. Give it only the case's `task` and the worktree path. Your own context already knows the answer, so an in-context replay is not evidence; without a way to dispatch, the case stays unproven. An edited plugin skill reaches a subagent only once the runtime has reloaded it; until then, pass the edited skill file to the subagent as the skill to follow.
3. Grade the resulting diff, then remove the worktree.

## Grading

A replay is **green** when the reviewer reports, or the author's diff avoids, the defect in `## Expected`: same object, same mechanism. Wording and line numbers may differ. An author run that avoids the defect by not doing the task is red. Record the verdict, the matching finding or diff hunk quoted, and the date in `results/<slug>.json`.

Agents vary between runs. A reviewer case is replayed once; replay it twice more when its verdict changes after an edit, and take the majority. An author case needs two green runs.

## Proving a prose edit

1. Write the case. Replay it against the prose **before** the edit: it must be red. A case that is already green shows the reader catches this now; keep it as a regression case and make no prose edit.
2. Edit the prose with a general rule.
3. Replay the case: it must be green. If it stays red, the rule is in the wrong place or too vague; revise it and replay. After two revisions that stay red, return it as a proposal with both replays.
4. Replay every other case of the same reader whose `guards` include the edited file. An edit that turns an older case red is not done.

Replays cost a review or an agent run each, so run them when prose changes, not on every PR.
