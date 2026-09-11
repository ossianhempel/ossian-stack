# Daily recovery watchdog

Read on bootstrap, HQ takeover, or repair of scheduled recovery. This watchdog
wakes HQ after inactivity; it does not coordinate project work itself.

## Ensure one global job

When the runtime exposes recurring automations, task listing, and cross-task
messaging, inspect existing automations before creating anything. Maintain one
job with stable identity `project-hq-daily-wake`. Create it only when absent;
otherwise update its registered-HQ list without duplicating the job.

Configure it as a standalone, projectless daily run in the user's local timezone.
Default to 08:00 when the user has not chosen a time. Use the cheapest suitable
model with low reasoning. In Codex, prefer `gpt-5.6-luna` with `low` reasoning for
both the automation and each follow-up turn when model override is supported.

Each registry entry contains:

- project name;
- exact HQ task address and host;
- ledger path or project identifier; and
- registration date.

On takeover, replace the old address for that project. Do not register the same
project or address twice. If the runtime cannot schedule or message tasks, record
`unavailable: <reason>` in the ledger and continue without inventing a cron file.

## Scheduled behavior

Each daily run:

1. Read the current pinned-task inventory.
2. Intersect it with the registered HQ addresses. Never infer HQ identity from an
   emoji or title alone.
3. Send one compact follow-up to every registered HQ that remains pinned, using a
   cheap model override when supported:

   `/project-hq`

   `Daily HQ wake: reconcile dispatching and active owners, continue every ready authorized queue item, and report only meaningful changes or human blockers. Stay quiet when the queue is empty and nothing changed.`

4. Skip unpinned or inaccessible entries. Report an access or delivery failure in
   the watchdog run rather than claiming the HQ woke.

The watchdog does not read project files, create owners, perform queued work, or
archive tasks and clean Git allocations. The addressed HQ turn does that with its
normal permissions and ledger. While an HQ has active items or a task is
`closeout-pending`, retain its runtime-specific short heartbeat instead of waiting
for the next daily run.
