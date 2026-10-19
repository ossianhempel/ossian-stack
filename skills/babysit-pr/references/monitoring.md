# Monitoring ownership

Choose one wait owner before monitoring. Status evidence always comes from the
bundled provider checker; a notification means inspect fresh evidence, not READY.

## Host PR activity subscription

When the host exposes a PR activity subscription that wakes this conversation,
use it and end the turn after currently actionable triage. Retain its handle and
confirmation. Take one bundled status snapshot on each wake, resolve new feedback
within the inherited scope, then return to that subscription. A confirmed native
watch replaces shell polling and recurring status tasks.

For GitHub, preserve the review-discovery window on this path: record the first
snapshot whose corresponding `decisions` entry is ready, its head, base branch, and
observation time. Those entries use the shared readiness policy; a status-only
report does not itself complete the discovery window. Read
the checker's default window from its help. A changed head/base or any non-ready
snapshot resets the observation. Readiness requires a second fresh ready snapshot
after the window and the feedback resolver's assessment of any newly published
feedback. For Azure, retain all readiness gates in `azure-devops.md`.
If no activity will wake you at the window boundary, use one host timer for that
boundary. Without a timer, report the
remaining discovery wait and the exact resume request; do not promise a timed wake.

Disarm the subscription and any boundary timer when handing work back. A failed
subscription call leaves the watch unarmed: inspect the error and use an available
fallback without claiming native monitoring is active.

## No PR activity subscription

Use the bundled polling command as the in-turn wait. Consume its output and exit
code, rearm it after fixes, and preserve its query-error budget and review window.
If a host scheduler is available and the turn must end, schedule one owner to take
bundled snapshots: minutes while CI or automation runs, 20–30 minutes while only
humans are pending, then hourly when unchanged. Disable that task at the stop
condition. If neither a subscription nor a scheduler can wake another turn, stay
on the bundled watcher until CI and detected automation settle, then hand back
with the exact resume request.

## Evidence and failures

The same checker runs across requests. After a tool timeout, resume the existing
process if it is still running; otherwise rerun the bundled command. Missing
dependencies or access
leave readiness unverified; report the concrete limitation and any readable state.
One-off forge reads are for diagnosis, not a replacement readiness verdict. Keep
query failures visible: an empty or unparsable result is unavailable evidence,
never success. Patch the shared helper when its verdict is wrong and verify that
failure there. Keep custom sleeps, repeated model-driven status reads, and temporary
watcher scripts out of the monitoring path.
