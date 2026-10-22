# Artifact lifecycle

Keep the working record in the host's durable plan or thread. Create a file only
when a tool needs one, resumption requires one, or it is part of the requested
result. Source changes, useful regression tests, and intended documentation are
deliverables; temporary plans, logs, fixtures, and prototypes are scratch.

## Before creating scratch

- Reuse the project's scratch convention, or allocate a unique task directory
  outside the repository. Keep scratch out of tracked product files and plugin
  caches. Check ignore rules explicitly when scratch must be inside the repo.
- Record the exact directory, repository, task identity, and cleanup action in
  the host's durable record before creating its contents. Record resources outside
  that directory separately, including owned processes and external test data.
- For a bounded command, arrange cleanup on success, failure, and catchable
  interruption using the runtime's cleanup facility. Abrupt process termination
  can bypass it: retain the exact directory in the durable record for recovery.
- Keep any necessary resume file within that owned directory. Its contents are
  the goal, decisions, completed checks, next step, and outstanding cleanup.
  Reuse existing durable project records instead of adding a second tracker.

## Simulators and devices

A simulator costs gigabytes of disk and outlives the session, so a leaked one is
the most expensive scratch an agent leaves. Reuse an existing device when the
check allows it; create one only when the check needs a clean or specific device.
Track ownership with `scripts/sim-ledger.py` (Python 3, wraps `xcrun simctl`),
anchored to this skill's directory and keeping the ledger in the task's scratch
directory:

```
SKILL_DIR="<absolute path of the ossian-mode directory>";
python3 "$SKILL_DIR/scripts/sim-ledger.py" begin "<task scratch directory>/sims.json"
```

- Run `begin` before the first build or test. The clones `xcodebuild` adds for
  parallel testing count as owned only when the test destination is a device
  the ledger owns and whose name no other device uses, so for parallel tests
  create the destination through the ledger with a distinct name. Other new
  clones may be Xcode.app's or another session's; `end` lists them and leaves
  them alone.
- Create or clone devices through the ledger (`create LEDGER NAME DEVICE_TYPE
  RUNTIME`, `clone LEDGER SOURCE_UDID NAME`), or `adopt LEDGER UDID` right after
  making one another way. Each prints the UDID to drive.
- At closeout run `end LEDGER`. It shuts down and runs `xcrun simctl delete` on
  owned devices only, then verifies they are gone; a non-zero exit names the
  leftovers to report. Test clones are skipped while any `xcodebuild` process
  runs, since another test run may own them; rerun `end` once it exits. A device you only booted is not owned: shut it down if
  you booted it, and leave it in place.
- Without Python, record each UDID in the durable record when it is created and
  run `xcrun simctl shutdown <udid>` then `xcrun simctl delete <udid>` for each
  at closeout. Never use `delete all`, `delete unavailable`, or `erase` on a set
  you share with the user.

## Closeout and recovery

Before reporting completion or closing cancelled work:

1. Put the concise result and necessary evidence in the final response or the
   project's existing durable record. Preserve requested deliverables and useful
   regression coverage. Scratch should not become an archive by default.
2. Stop only task-owned processes, reverse temporary instrumentation, and clean
   task-created fixtures using their scoped cleanup actions. Remove the exact
   owned scratch paths with the project's deletion convention; use Trash where
   available. Preserve pre-existing files and unrelated edits. Never infer
   ownership from age or a broad filename pattern.
3. Verify those paths are absent and owned resources are stopped or restored.
   Inspect the final diff and untracked files for accidental artifacts; also check
   registered ignored and external paths, which Git status cannot prove clean.
4. Mark cleanup complete only after those checks pass. If cleanup fails, report
   the exact leftover and reason as unfinished work; keep its recovery entry.

On resumption after interruption, reconcile the recorded paths and resources
before creating replacements. Clean leftovers no longer needed and retain only
what the active task still requires. A pause or handoff keeps a named cleanup
owner and the next cleanup action in the durable record. A resumed task cannot
close until its outstanding cleanup is verified.
