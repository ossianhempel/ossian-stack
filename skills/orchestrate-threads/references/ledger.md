# The ledger

`docs/agents/hq.md` in the project. HQ creates it on bootstrap and rewrites it
whenever a workstream changes. It is short and structured, because it is parsed
by the next `/orchestrate-threads`, not read for pleasure. Do not write anything here
that lives in a ticket, a spec, or a PR; link instead.

Whether it is committed is the user's call. Say once at bootstrap that it
contains thread names and nothing secret.

```markdown
# HQ · <Project>

Runtime: <runtime name> · delegation level: <1|2|3> · probed: <date>
Tracker: <link to docs/agents/issue-tracker.md, or "none">
HQ thread: `<project emoji> <Project>`

## Open workstreams

| Workstream | Thread | Kind | State | Last report | Waiting on |
| --- | --- | --- | --- | --- | --- |
| <name> | `<Project> · <name>` | plan | wayfinder in progress | <date>: <one line> | <human decision / nothing> |
| <name> | `<Project> · <name>` | build | PR open, babysit running | <date>: <one line> | review |
| <name> | pending | diagnose | brief handed to user | never | user to create thread |

## Blocked on the human

- <name>: <the decision, one line>

## Done

| Workstream | Artifact | Closed | Thread |
| --- | --- | --- | --- |
| <name> | <PR or doc link> | <date> | archived (done) |
| <name> | none | <date> | archived (dead end: <one line>) |
| <name> | <spec link> | <date> | archive pending, user to do |

## Inline edits

- <date>: <what and why, one line>
```

Rules:

- One row per workstream, keyed by the workstream word chosen when the row is
  created; it never changes. Only the HQ thread in the header carries an emoji.
- `Kind` is the work type, one of plan, build, babysit, diagnose. How it ran
  is the `Thread` column, never the kind.
- `Thread` is the exact title, or `pending` for a level 2 thread the user has not
  yet created, or `subagent` for a level 3 run.
- `Last report` is a date and one line, not the report.
- The blocked list names workstreams by name, never by ticket number.
- `Thread` in the done table says whether the thread was archived and why
  (done, redundant, dead end), or `archive pending, user to do` when the
  runtime cannot archive from HQ.
