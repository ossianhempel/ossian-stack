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
