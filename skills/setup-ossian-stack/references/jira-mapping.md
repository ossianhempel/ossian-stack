# Optional existing-Jira mapping

Create `docs/agents/jira-mapping.md` only when an existing Jira convention
differs from the defaults in the Jira tracker template. Omit the file for a
fresh setup. Omit every row whose concept still uses its default. A missing row
keeps the original behavior.

Use this deterministic table, sorted by Concept:

| Concept | Representation | Value | Read | Apply |
| --- | --- | --- | --- | --- |
| `<semantic path>` | `<label, status, field, body, relationship, or query>` | `<exact existing value>` | `<exact read/test operation>` | `<exact existing write operation>` |

Stable concept paths:

- `triage.category.bug`, `triage.category.enhancement`
- `triage.state.needs-triage`, `triage.state.needs-info`
- `triage.state.ready-for-agent`, `triage.state.ready-for-human`, `triage.state.wontfix`
- `ticket.create.type`
- `pickup.frontier`, `pickup.claim`, `pickup.blocked`, `pickup.paused`, `pickup.done`
- `wayfinder.map`, `wayfinder.membership`, `wayfinder.kind.research`
- `wayfinder.kind.prototype`, `wayfinder.kind.grilling`, `wayfinder.kind.task`
- `wayfinder.claim`, `wayfinder.blocking`, `wayfinder.complete`

`Value` identifies a value that already exists in the host system. `Read` says how
to recognize it. `Apply` says how to write it without changing the tracker schema.
A body fallback is a valid override when the default label or native relationship
would introduce unapproved vocabulary. Do not add rows for repository branch,
commit, PR, permission, credential, API/CLI, or reporting conventions; those stay
in `docs/agents/issue-tracker.md` as the selected tracker's ordinary configuration.
