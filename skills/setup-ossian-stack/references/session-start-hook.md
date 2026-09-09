# Session Start Hook

Read for hook feature readiness and host trust approval. Follow the scope and safety contract in the skill entry point.

## 4. Approve session-start hooks

This plugin currently ships no active default hooks in `hooks/hooks.json`. If hooks are configured locally or added in the future, follow this approval checklist.

Check the two independent runtime gates in order:

1. **Hooks feature enabled.** Some runtimes disable plugin hooks globally. When
   disabled, no trust prompt can appear. Point the user at the runtime's supported
   feature/configuration flow, enable it only with their approval, then restart.
2. **Hook approved.** Some runtimes pin hooks to a content hash and require explicit
   trust approval. Show the user what the hook does and use the runtime's approval
   flow. Do not edit trust state by hand.

Report these separately. “Hook valid” does not mean active when the feature is
disabled, and “feature enabled” does not mean the shipped hash is trusted.
