---
name: resolving-merge-conflicts
description: "Use when you need to resolve an in-progress git merge/rebase conflict."
---

1. **See the current state** of the merge/rebase. Inventory conflicting files plus unrelated staged and unstaged work; check git history and the operation state.

2. **Find the primary sources** for each conflict. Understand deeply why each change was made, and what the original intent was. Read the commit messages, check the PRs, check original issues/tickets.

3. **Resolve each hunk.** Preserve both intents where possible. Continue where the intended resolution is clear. Do **not** invent new behaviour. If preserving both intents needs a product decision, leave the conflict state intact and explain the decision needed. Abort only when requested or authorized.

4. Discover the project's **automated checks** and run them, typically typecheck, then tests, then format. Fix anything the merge broke.

5. **Finish the merge/rebase.** Stage only files resolved for this operation; preserve unrelated staged and unstaged work. Complete the requested merge/rebase after validation only within inherited authority. Inspect the index before any commit so unrelated staged changes are not included; use an isolated checkout or pause completion if they cannot safely be excluded. A no-commit request leaves the validated resolution uncommitted. Continue a rebase only when its commit/history changes are authorized.
