# Targeted Mode

Parse the specific URL for the host, owner, repository, PR number, comment ID,
and fragment type. Keep that identity on every forge call. In the examples, set
`HOST` to the host from the URL. The API calls use the PR's base repository,
including for a fork-to-upstream PR.

Use only the edit, commit, push, reply, and resolve actions granted by the
request or inherited from the caller. A linked comment sets the target.

## Top-level comment

For `https://HOST/OWNER/REPO/pull/NUMBER#issuecomment-COMMENT_ID`, fetch only the
linked top-level comment.

```bash
gh api --hostname "$HOST" repos/OWNER/REPO/issues/comments/COMMENT_ID \
  --jq '{id, issue_url, html_url, author: .user.login, body}'
```

Verify the returned comment ID and `issue_url` against the selected repository
and number. Also require `html_url` to identify the same host, repository, and
`/pull/NUMBER#issuecomment-COMMENT_ID` as the requested link. The Issues API
also serves ordinary issue comments, whose web path has `/issues/`. Stop on
a missing comment, mismatched identity, or unavailable API.

Before judgment or edits, look for a substantive prior reply about this comment
from the acting identity. GitHub returns a flat comment list. Read every page
of that list for both this check and the pre-post recheck. Filter in the API
client to replies that link or explicitly reference the target comment, and
inspect only the matches. Use the completion checks below to resume only the
remaining authorized actions.

Use the judgment steps below for any remaining feedback. When authorized to
reply, check again for a satisfying reply that may have appeared during the
run. If a reply is still needed, post a top-level PR comment quoting the
relevant passage and linking the original comment. Read it back by its
returned ID and verify its PR identity and body. Report the linked comment's
verdict and any verified reply. Skip review-draft checks, thread resolution,
and the full PR sweep.

## Inline review thread

For `https://HOST/OWNER/REPO/pull/NUMBER#discussion_rCOMMENT_ID`, resolve the
comment to its thread. For the inline examples and the shared Full Mode commands,
set `GH_HOST` to the parsed GitHub Enterprise host. On github.com, omit the
environment prefix.

**Step 1** -- Get comment details and GraphQL node ID via REST (cheap, single comment):
```bash
GH_HOST=<host> gh api repos/OWNER/REPO/pulls/comments/COMMENT_ID \
  --jq '{node_id, path, line, body}'   # omit GH_HOST=<host> on github.com
```

**Step 2** -- Map comment to its thread ID. Use [scripts/get-thread-for-comment](../scripts/get-thread-for-comment). Set `SKILL_DIR` to the absolute directory you loaded the resolve-pr-feedback SKILL.md from, the Bash tool's CWD is the user's project, not the skill dir, and shell state does not persist between Bash calls, so set it inline. If the bundled script is missing, use Full Mode's fallback `gh` commands to inspect the PR comments:
```bash
SKILL_DIR="<absolute path of the directory containing the resolve-pr-feedback SKILL.md>";
GH_HOST=<host> bash "$SKILL_DIR/scripts/get-thread-for-comment" PR_NUMBER COMMENT_NODE_ID [OWNER/REPO]
```

This fetches thread IDs and their first comment IDs (minimal fields, no bodies) and returns the matching thread with full comment details.

## Judge, Fix, Reply, Resolve

Before judging or editing either comment type, check the current PR head,
visible replies about the target, and the inline thread's resolution state.
Use the caller's current request and any decisions they supplied.

- A claimed fix is complete after you verify it still works on the current
  PR head. A later change can remove it even if the original commit is present.
- An existing reply satisfies the reply action while its verdict still applies.
  If the reply requested a human decision, use the decision now supplied to
  judge what remains. While it is outstanding, report the pending decision
  and keep any inline thread open.
- Resolve an inline thread only when the caller authorized resolution and a
  verified visible reply records a current verdict that permits it. If only
  resolution remains, resolve and read back that thread. If the verdict is
  unclear, keep the thread open until you have enough evidence to judge it.

Report completed work and act only on the remaining authorized steps. If the
requested work is complete, stop.

**Judge first (the gate).** Apply the rubric in `references/evaluation-rubric.md` to this item, in your own context. For an inline thread, account for `isOutdated` and the location fields (`line`, `originalLine`, `startLine`, `originalStartLine`) -- targeted threads can be outdated too and need the same relocation handling. The cross-item reasoning in the rubric is a no-op for a single thread, but the read-depth and divert logic apply in full: deep-read (callers, invariants, `git blame`/PR rationale for author intent) before accepting a contestable finding or overriding code that looks deliberate. This is the legitimacy check, don't fix on the reviewer's authority alone.

**Then act on the verdict:**

Confirm edit authority before dispatching a fixer or changing files. For a
triage-only or reply-only request, report warranted changes as recommendations
and send a reply only when authorized.

- **`fixed` / `fixed-differently`**, read `references/agents/pr-comment-resolver.md` and spawn a single generic subagent seeded with that fixer prompt to implement it. Do not dispatch a standalone agent by type/name. Pass the file/location fields (resolved location or anchor if outdated), the comment text, and your note on what to change and why it's valid. The fixer is a pure executor. **When the harness exposes no way to dispatch (or the dispatch fails), apply the fix yourself in this context**, using that same prompt as your own instructions, the fixer implements a change this step already approved, so running it here costs nothing but the separate context (see Full Mode step 4).
- **`replied` / `not-addressing` / `declined`**, no subagent. Compose the reply text per the rubric and proceed to the reply step for the selected comment type.
- **`needs-human`**, compose `decision_context` and the natural-sounding reply per the rubric, leave any review thread open, and report the decision for the user or caller. The shared reply step below posts the reply once, do not post it here.

Use [Full Mode steps 5 and 6](full-mode.md) for validation and authorized
commit or push when code changed. For a top-level comment, use the reply and
readback above.

## Post an authorized inline reply

Check for your own unsubmitted review immediately before posting a new inline
reply. A pending review can absorb the reply and keep it invisible to the
reviewer. Paginate the reviews and select pending IDs.

```bash
GH_HOST=<host> gh api --paginate repos/OWNER/REPO/pulls/PR_NUMBER/reviews --jq '.[] | select(.state == "PENDING") | .id'
```

If a pending ID is present, report that the unsubmitted review blocks the
reply and stop at that point. The user owns the draft.

Follow [Full Mode step 7](full-mode.md) to post and verify the authorized reply,
then resolve only when authorized and the verdict permits resolution. Read
back only the targeted thread.
