# Earlier thread (compacted summary — the full transcript is gone)

> Summary of prior conversation: The user asked to migrate gainslog's workout sync from polling to Convex subscriptions. The assistant replaced `usePollingSync` with `useSyncSubscription` across 6 screens, added a temporary `console.log('[sync-debug]', ...)` in `src/sync/subscription.ts` to trace duplicate events, found and fixed a duplicate-write bug caused by the effect re-subscribing on every render, and stashed an unrelated experiment ("try batching writes") with `git stash`. It created a scratch branch `scratch/sync-repro` to reproduce the duplicate bug. The user approved and the assistant opened PR #118 on branch `feat/sync-subscriptions`. The assistant noted that offline-to-online reconnection was not tested on a real device, only in the simulator. The user asked whether the old `usePollingSync` hook should be deleted now or in a follow-up; this was not answered before the summary.

# Live state (what tools return right now)

`git branch --show-current`: `main`

`git status`: clean

`git stash list`:
```
stash@{0}: On feat/sync-subscriptions: try batching writes
```

`git branch`:
```
* main
  feat/sync-subscriptions
  scratch/sync-repro
```

`gh pr view 118`:
```
title: feat(sync): move workout sync to Convex subscriptions
state: MERGED (2 days ago)
```

`rg "sync-debug" src/`:
```
src/sync/subscription.ts:41:    console.log('[sync-debug]', event.id, event.kind);
```

`rg -l "usePollingSync" src/`:
```
src/sync/usePollingSync.ts
```
