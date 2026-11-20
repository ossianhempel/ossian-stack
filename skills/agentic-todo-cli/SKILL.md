---
name: agentic-todo-cli
description: "Read, capture, schedule, and update Agentic Todo tasks, projects, areas, tags, and sync with the agentic-todo CLI. Use when the user asks to check or change their Agentic Todo tasks from a terminal or agent."
---

# Agentic Todo CLI

`agentic-todo` reads and writes the user's Agentic Todo account from a terminal.
It signs in to the same account as the Mac and iPhone apps and keeps its own
synced local copy, so the Mac app does not need to be running. The binary is the
source of truth: run `agentic-todo help GROUP` or `agentic-todo COMMAND --help`
before relying on a flag this skill does not show.

Done means the requested change is visible when you read the record back, and the
command reported that the change reached the cloud.

## Setup

1. `agentic-todo --version`. If it is missing, use the copy the Mac app bundles at
   `Agentic Todo.app/Contents/MacOS/agentic-todo`, or install it with
   `brew install ossianhempel/tap/agentic-todo` once a release is published.
   From a checkout of the app repo, `./script/install_cli.sh` installs into
   `~/.local/bin`.
2. `agentic-todo auth status --json`. If it is not signed in, run
   `agentic-todo auth login`. It prints a URL and a short code. Give both to the
   user, who approves in a browser with the same account as the app. Wait for the
   command to finish; the code expires after about 10 minutes.
3. The CLI never shows a Keychain dialog. If it exits 5 asking for `auth login`,
   the stored token is unreadable by this build: run `auth login` again.

Never pass tokens as arguments, never read `.env` files for them, and never touch
the app's `workspace.sqlite`. `--database PATH` is only for scratch stores you
created with `agentic-todo init --database PATH`.

## Safe write workflow

1. **Read** with `list`, `search QUERY` or `show ITEM`, using `--json`.
2. **Identify** the record by ID (a full UUID or a unique prefix of 8+ chars).
   If several records match a title, show them to the user and ask. Never guess.
3. **Preview** risky writes with `--dry-run`.
4. **Write** by ID. Pass the `revision` you read as `--revision N` when time
   has passed since the read; a stale revision exits 4 instead of overwriting.
5. **Verify** with `show ITEM --json`.

Reads never authorize writes. Trash, checklist removal, ending a series and sync
decisions ask for confirmation; in a non-interactive shell pass
`--force --no-input`, and only for what the user asked.

## Commands

```sh
agentic-todo list --view today --json            # also inbox, evening, upcoming, anytime, someday, blocked, logbook, trash, all
agentic-todo list --project PROJECT --kind task --json
agentic-todo search 'proposal' --json
agentic-todo show ITEM --json

agentic-todo capture 'Write proposal tomorrow @Launch /Writing #work'   # Quick Add parsing
printf '%s\n' 'Call accountant next Monday' | agentic-todo capture - --json
agentic-todo task add 'Literal title' --notes 'No date parsing here'
agentic-todo project add 'Launch'
agentic-todo heading add 'Writing' --parent PROJECT

agentic-todo item edit ITEM --title 'Final proposal' --revision 3
agentic-todo item move ITEM --area AREA          # or --parent PROJECT_OR_HEADING, or --inbox
agentic-todo item complete ITEM                  # exit 6 when prerequisites block it
agentic-todo item reopen ITEM
agentic-todo item trash ITEM --force --no-input
agentic-todo item restore ITEM

agentic-todo task schedule ITEM --date 2026-11-02 --time 09:00
agentic-todo task schedule ITEM --deadline 2026-11-20
agentic-todo task schedule ITEM --date 2026-11-02 --repeat week --weekdays 2,5
agentic-todo task schedule ITEM --evening        # or --someday, --clear
agentic-todo task reschedule ITEM --date 2026-11-03   # recurring tasks only
agentic-todo task occurrences ITEM --limit 10 --json

agentic-todo area list --json
agentic-todo tag set ITEM --tags 'work,writing'  # --tags='' clears
agentic-todo checklist add ITEM --title 'Step 1'
agentic-todo checklist edit ROW --completed true
agentic-todo dependency add ITEM --blocker PREREQUISITE
agentic-todo activity list --json
agentic-todo activity undo EVENT

agentic-todo sync status --json
agentic-todo sync now --timeout 120
```

Dates are `YYYY-MM-DD`, times 24-hour `HH:MM`. `--weekdays` uses 1=Sunday
through 7=Saturday. `capture` parses dates, `@Project`, `/Heading` and `#tag`;
`--literal` keeps the text as typed. `task add` and `item edit` never parse.
To move a one-off task's date, use `task schedule`, not `task reschedule`.
Creation accepts `--id UUID`; reuse the same ID when retrying a creation whose
response was lost, so no duplicate appears.

## Output and errors

Use `--json` for anything you parse. Success is
`{"version":1,"ok":true,"data":…}`; failure has `error.kind`, `error.message`
and `error.exitCode`. `--plain` prints tab-separated list rows:
`id kind title name revision state intent`.

| Exit | Meaning | What to do |
| --- | --- | --- |
| 2 | Bad syntax or input | Read the message; check `--help` |
| 3 | Record not found | Re-read; the ID may be wrong or trashed |
| 4 | Revision conflict | Re-read the record, then retry with the new revision |
| 5 | Sign-in or confirmation needed | `auth login`, or add `--force --no-input` if the user asked |
| 6 | Blocked by prerequisites | Report the blockers; don't force it |
| 7 | Busy | Another CLI process holds the lock; retry shortly |
| 8 | Schema too new | Update the CLI |

Commands pull before they run and upload afterward. If a write exits 1 with
`data.appliedLocally: true` and `data.cloudSynced: false`, the change is saved
locally. Do not repeat it; run `agentic-todo sync now` to upload it.

## App-only commands

`--app` talks to the running Mac app instead of the cloud copy, for things that
are deliberately device-local: agents and their permissions, approvals, and app
settings. It needs the app's window open and signed in to the same account. Use
the app's bundled binary for `--app`; a standalone install cannot reach the
signed app's data.

```sh
agentic-todo --app approval list --json
agentic-todo --app approval approve APPROVAL
agentic-todo --app permission set AGENT --capability createTask --mode ask
```

The CLI's own sign-in grants full account-owner access. Tell the user that when
setting it up for another agent.
