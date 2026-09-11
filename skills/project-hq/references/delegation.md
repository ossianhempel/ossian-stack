# Delegation surfaces

Execution owners are behind HQ. Choose the owner that preserves continuity,
isolation, and useful parallelism. The user continues to communicate only in HQ.

## Probe

Inspect the current runtime for these capabilities and record the result in the
ledger:

| Capability | Why HQ needs it |
| --- | --- |
| Create a task or session, optionally in a worktree | Durable workstream owner |
| Spawn a subagent that returns to HQ | Bounded parallel owner |
| Read and wait on an owner's current state | Quiet monitoring and recovery |
| Send a cross-task follow-up | Decisions, corrections, and later queue items |
| Set title, pin, and archive | Stable HQ identity and owner cleanup |
| Run recurring work | Daily recovery and active-work heartbeat |

Tool names and availability change, so verify capabilities instead of inferring
them from the host name. A `/project-hq` invocation authorizes creating the
execution owners needed for the tasks the user supplies. It does not grant any
repository, publication, tracker, release, or destructive action absent from the
task's scope.

## Choose an owner

1. Do a trivial authorized action in HQ when it has one obvious change and no
   isolation rule forbids it. Record its queue item and evidence without creating
   an owner.
2. Reuse the existing workstream owner when it remains accessible and suitable.
3. Use a durable task in a separate worktree for ongoing implementation, work
   likely to need follow-up, or work whose history and environment must persist.
4. Use a subagent for bounded research, review, diagnosis, or implementation that
   can return a complete report or diff to HQ in one run.
5. If no owner surface exists, HQ may execute a bounded task itself unless a
   checkout-isolation rule forbids it.

Never hand the user a brief to paste into another task as a normal fallback. If a
required isolated environment cannot be created, keep the queue item blocked in
HQ and state the exact missing capability.

Before creating any owner, reconcile its queue item against live tasks, branches,
PRs, documents, and prior dispatch records. Record `dispatching`, create the owner,
then store its exact address and mark the item active. A partial failure remains
recoverable and is inspected before retry.

## Return address

Every initial brief and later assignment contains HQ's exact name, address, and
available return channel. The owner reports proactively when it finishes, becomes
blocked or stuck, needs human input, or reaches its authorized stop boundary.
Use cross-task messaging when available. A subagent returns through its result.
When HQ can read but cannot message a durable task, the task's final structured
report is the return channel; HQ records any follow-up as blocked rather than
asking the user to transport it.

Workers never address the user directly. They prepare decision-ready questions
with evidence and a recommendation for HQ. Only HQ asks the user and returns the
answer to the owner.

Authority belongs to the queue item, not to one session. After proving an owner is
inactive and its artifact is recoverable, HQ may transfer the item and its existing
authority to one replacement owner. Record the transfer before continuing and
retire the old ownership record. Never run both owners against the same artifact.
When neither continuation nor safe transfer is possible, ask in HQ only for the
missing access or disposition decision. Do not suggest that the user inspect,
message, or operate the unreachable owner.

## Runtime guidance

- **Codex app:** prefer project tasks in separate worktrees for durable repository
  work. Use subagents for bounded parallel work. Use task reads, waits, messages,
  titles, and archive controls when present. Keep execution tasks unpinned.
- **GitHub Copilot app:** verify a distinct session and worktree before repository
  mutation. Fleet and custom agents are bounded owners, not substitutes for
  required checkout isolation. If isolation cannot be proved, block the item in
  HQ.
- **Claude Code:** use worktree or background agents for bounded execution. When a
  durable sibling session cannot be created programmatically, retain the work in
  an agent or HQ rather than making the user manage a second interface.
- **Other runtimes:** choose from observed capabilities and preserve the same
  sole-interface and recovery rules.

## GitHub Copilot isolation and PR-link recovery

Record HQ's original checkout path and branch. Before an owner changes files,
verify that its session identity and worktree differ from HQ. An in-place session,
same-checkout fork, or instruction to switch HQ's branch is not isolated.

Transfer only an authorized diff or snapshot into the owner and require receipt.
The owner must preserve unrelated dirty work and must not mutate HQ's checkout.
Carry existing delivery authority through the transfer.

If HQ is already PR-linked or its title reverts, inspect supported detach controls.
Use a supported detach only within existing authority. Do not edit private runtime
metadata. If no safe detach exists, keep coordination here until the user
explicitly establishes a replacement HQ, then update the ledger and daily registry
without losing the old task or its recoverable work.
