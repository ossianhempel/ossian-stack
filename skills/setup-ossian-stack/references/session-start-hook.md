# Session Start Hook

Read for hook feature readiness and host trust approval. Follow the scope and safety contract in the skill entry point.

## 4. Approve the session-start hook

This plugin ships one hook: a session-start nudge for `continual-learning`. It
reads transcript counts and writes nothing the user owns.

Check the two independent runtime gates in order:

1. **Hooks feature enabled.** Some runtimes disable plugin hooks globally. When
   disabled, no trust prompt can appear. Point the user at the runtime's supported
   feature/configuration flow, enable it only with their approval, then restart.
2. **Hook approved.** Some runtimes pin hooks to a content hash and require explicit
   trust approval. Show the user what the hook does and use the runtime's approval
   flow. Do not edit trust state by hand.

Report these separately. “Hook valid” does not mean active when the feature is
disabled, and “feature enabled” does not mean the shipped hash is trusted.

The hook needs `jq`. Without it, it exits silently and nothing else breaks.
