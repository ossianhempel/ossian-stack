---
name: postq-bridge
description: "Bridge Content Factory output into Post Queue. Use whenever an agent needs to inspect PostQ context, generate or select Content Factory posts, create PostQ drafts, or schedule Walkmon TikTok posts through PostQ while preserving TikTok inbox-draft/manual-finish delivery."
---

# PostQ Bridge

Use this skill to move approved Content Factory artifacts into Post Queue without browser automation. Content Factory owns creative generation and `status.json`; Post Queue owns media uploads, drafts, schedules, Post Targets, notifications, and publishing history.

The proving path is Walkmon video:

1. Inspect PostQ context.
2. Inspect Content Factory context.
3. Generate or select approved Walkmon video output.
4. Upload the MP4 to PostQ.
5. Create a PostQ draft.
6. Stop for approval.
7. Schedule the post to both TikTok (inbox draft) and Instagram (reel for video, feed carousel for slides) on the same slot.

Direct TikTok API publishing is outside this skill's default path. Prefer TikTok inbox draft delivery so the user can finish in the TikTok app, add native text/audio, and avoid the engagement downside of server-side direct publishing. The one sanctioned TikTok exception is the two overnight slots declared in Content Factory's `configs/posting-goals.json`, covered under "Night slots publish directly" below.

**Instagram is a permanent part of the schedule now.** Content Factory declares an `instagram` channel goal for Walkmon and GainsLog in `configs/posting-goals.json` with the same slot times as TikTok. An approved set therefore schedules **two targets on one post**: a TikTok inbox draft (caption pasted by hand) and an Instagram target (caption attached automatically, since the Graph API publishes directly). The IG format follows the media -- `reel` for a Walkmon video, `feed` for a slideshow -- and a slideshow additionally needs the 4:5 media variant. See "Every scheduled post carries two targets on one slot" below. Instagram has no inbox-draft state, so IG is always a direct publish; there is no caption-paste step on IG.

## Repos

Work from explicit repo roots, but **resolve them, do not hardcode them.** These repos are siblings by convention, not at a fixed absolute path, and the convention breaks on any other machine, in a worktree, or under a different checkout layout.

Resolve once at the start of a session and reuse the variables:

```bash
CF="${CONTENT_FACTORY_DIR:-$(cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)/.." && pwd)/content-factory}"
PQ="${POST_QUEUE_DIR:-$(dirname "$CF")/post-queue}"
SKILL="$(readlink -f ~/.claude/skills/postq-bridge 2>/dev/null || echo ~/.claude/skills/postq-bridge)"

for d in "$CF" "$PQ" "$SKILL"; do [ -d "$d" ] || echo "MISSING: $d"; done
```

If any path is missing, **ask the user where the repo lives.** Do not guess, and do not report the pipeline as broken because a directory was not where you assumed.

When changing this skill, edit the canonical source that `$SKILL` resolves to (the `ossian-stack` checkout). The runtime copy under `~/.claude/plugins/cache/ossian-stack/` is regenerated on every marketplace refresh, so edits there are lost. Do not edit generated runtime copies under app repos either.

## PostQ Auth

Use the existing `postq` config resolution first. If credentials are missing, use the Post Queue 1Password item without printing secrets:

```bash
export POSTQUEUE_API_URL=https://postqueue.social
export POSTQUEUE_API_TOKEN="$(op read "op://Development/Post Queue/postq-token")"
```

Prefer environment/config over `--token` so bearer tokens do not land in shell history. Never print `.env`, token values, OAuth payloads, or provider responses containing secrets.

**Post Queue runs in production at `https://postqueue.social`. Target that, not localhost.**

`postq` is a client, not a server. `src/cli/config.ts` resolves `apiUrl` in this order:

```
--api-url  >  POSTQUEUE_API_URL  >  ./.postqrc.json  >  ~/.config/postq/config.json  >  DEFAULT_API_URL
```

`DEFAULT_API_URL` is `http://localhost:3000`, a **dev-only fallback**. It is what you get when nothing else is set, and it is the wrong target for normal work. Verify what you resolved to before diagnosing anything:

```bash
pnpm --silent postq -- auth status --json --verbose   # prints POSTQUEUE_API_URL=...
```

If that shows `localhost:3000` and no local dev server is deliberately running, the URL is the bug. Set `POSTQUEUE_API_URL=https://postqueue.social`.

Failures and what they actually mean:

- `missing_token: POSTQUEUE_API_TOKEN is required` — no token in env or config. `op read` needs Touch ID or a service-account token, so it fails in a non-interactive shell. Ask the user rather than retrying blind.
- Connection refused on `localhost:3000` — you are pointed at the dev fallback, not at production. Fix the URL. Do not start the user's dev server to satisfy a misconfigured client.
- 401/403 against `postqueue.social` — real auth failure. The token is missing, wrong, or expired.

## Context Intake

Read PostQ state before creating anything:

```bash
pnpm --silent postq -- auth status --json
pnpm --silent postq -- accounts list --json
pnpm --silent postq -- drafts list --json
pnpm --silent postq -- posts scheduled --json
pnpm --silent postq -- posts recent --range 48h --status all --json
```

**Prefer `posts scheduled` and `posts recent` over `posts list --status`.**
`posts list` returns post-level rows only: no account, no per-target state, and
no failure reason, so a post whose only target failed still reads as a post
sitting in some status. The two newer commands resolve the target rows.

- `posts scheduled` returns every post with a non-terminal target (queued,
  uploading, publishing), oldest first, each target carrying `accountUsername`,
  `provider`, `format`, `scheduledFor`, `nextAttemptAt` and `attemptCount`.
  This is the correct answer to "what is going out, to which account, when".
- `posts recent [--range 24h] [--status successful|failed|all]` is the readback.
  It reports `counts.successful` / `counts.failed` for the window and, for each
  target, the field that actually matters after a failure:

```bash
# What went out, and what broke, in the last two days
pnpm --silent postq -- posts recent --range 48h --status failed --json
```

**The failure text lives in `targets[].failureReason`, not `lastError` or
`error`.** Reading the wrong key returns `(none)` and makes a hard failure look
like a post with no diagnosis. `posts show <postId> --json` returns the same
target shape for a single post when you need the media list alongside it.

A worked example of why this matters: a GainsLog slideshow failed twice on
consecutive days, and `posts list` showed only `status: failed` with an empty
`targets: {}`. `failureReason` on the target held the whole diagnosis, `TikTok
photo post failed: 400 - invalid_params: The request post info is empty or
incorrect`, which is a photo-carousel-only fault. Video was unaffected
throughout.

Read Content Factory state:

```bash
npx tsx src/cli.ts status --app walkmon
```

**Sets marked `⏳` are already queued downstream. Stop, do not re-upload them.**
The `handoff` block in their `status.json` records target, scheduled time, and
the PostQ ids. Uploading one again creates a second draft for media that is
already scheduled. If the downstream post was genuinely cancelled, clear the
record first and say so:

```bash
npx tsx src/cli.ts mark-handoff -s <set> -p tiktok --withdraw --note "cancelled in PostQ"
```

Use the context to avoid duplicate drafts or conflicting schedules. Resolve the accounts from `accounts list`: each app has a TikTok account (`Walkmon`, `GainsLog`) and an Instagram account (`walkmon.app`, `gainslog.app`). If a needed account is not connected, ask the user which account to use or whether to connect one, rather than guessing. If exactly one connected TikTok account exists, use it but include the account id and username in the draft summary before scheduling.

## Generate Or Select Content

Only hand off approved Content Factory output. "Approved" is a recorded state, not a judgement you make:

```bash
python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get('review'))" \
  "$CF/output/<set>/status.json"
```

`review.state` must be `"approved"`. The user sets it in the Content Factory dashboard (`npx tsx src/cli.ts serve` → Outputs tab), which also records their `feedback` and `updatedAt`. Treat `pending` or `changes_requested` as a stop: report it, ask them to review, do not upload.

Re-rendering a set clears its approval, because the asset that was approved is no longer the asset on disk. If you regenerate anything, it needs re-approval.

A complete, approved Walkmon set looks like:

- `output/<set>/<set>.mp4`
- `output/<set>/post.md`
- `output/<set>/status.json` with `review.state: "approved"`
- `output/<set>/review.md` when the `content-review` loop generated it

If no approved output is available, run the repo-local Content Factory review loop instead of drafting directly:

```text
/content-review
```

Walkmon mode drafts hook/reveal/caption copy, validates, reviews, renders, and writes `review.md`. Do not use `assemble-video` unless the user explicitly asks for the unvetted fast path.

## Parse Content Factory Copy

Use the bundled parser so captions and on-video text are not hand-copied from Markdown:

```bash
node "$SKILL/scripts/parse-content-factory-post.mjs" \
  "$CF/output/<set>/post.md"
```

It emits:

```json
{
  "title": "<set>",
  "platformTitle": "Short title for TikTok photo metadata",
  "caption": "Caption text\n\n#hashtags",
  "onVideoText": [
    { "label": "Text 01 (video clip)", "text": "..." },
    { "label": "Text 02 (still image)", "text": "..." }
  ]
}
```

Keep the on-video text in the final summary, but check first whether it is already on the video. Content Factory bakes on-video text into the MP4 **by default** (`defaults.bakeText`, default `true`), so `onVideoText` is usually a description of what the viewer already sees, not a to-do for the user.

Determine which case you are in from the set's config and its `post.md` header:

- Baked (default): `post.md` opens "On-video text is already baked into the MP4". Report the blocks as reference only. Do not tell the user to add them.
- Not baked (`--no-bake-text`, `defaults.bakeText: false`, or per-set `"bakeText": false`): `post.md` opens "Text below is added manually". Report the blocks as work the user still has to do in the native editor.

Captions are never baked. They always get pasted into TikTok/Instagram.

## Copy Is Transported, Not Authored

This skill moves approved copy. It does not write or revise it. The caption, hashtags,
and on-video text in `post.md` already passed Content Factory's lints, the
`ai-slop-reviewer` slop gate, and a human approval in the dashboard. Pass them through
verbatim from the parser output.

If the copy needs to change for any reason (too long for the platform, wrong hashtags, a
claim the user disputes, a caption that reads badly on re-reading), **do not edit it
here.** Editing in the bridge produces copy that no lint and no human ever approved,
while `status.json` still says `approved`. Instead:

1. Stop and tell the user what needs to change and why.
2. Fix it at the source in the Content Factory config, using `/copywriter` for Walkmon
   video copy or `/slideshow-creator` for slide sets, then re-run the slop lint:
   `python3 <ai-slop-reviewer>/scripts/ai_slop_lint.py -`.
3. Re-render and get re-approval. Re-rendering clears approval by design.

The one safe exception is deleting a platform's own prefill text, such as TikTok's
`#PostQueue`. That removes something Content Factory never wrote; it does not change
approved copy.

## Create The PostQ Draft

Upload the generated MP4 from the Post Queue repo:

```bash
pnpm --silent postq -- media upload "$CF/output/<set>/<set>.mp4" --json
```

**Check every upload returned an id.** `postq` exits non-zero and writes the
reason to stderr, so the CLI is not the problem, but the obvious shell idiom
throws that away:

```bash
# WRONG: 2>/dev/null eats the reason, and the pipe means $? is the parser's
id=$(postq media upload "$f" --json 2>/dev/null | jq -r .mediaAssetId)
```

A batch written that way carried on past two failures with an empty `id`,
produced drafts with no media, and only surfaced as `validation_failed: Media
validation failed` at schedule time. The real error was
`upload_failed: Storage limit reached`. Keep stderr and assert the result:

```bash
out=$(postq media upload "$f" --json) || { echo "upload failed: $f"; exit 1; }
id=$(printf '%s' "$out" | jq -r '.mediaAssetId // empty')
[ -n "$id" ] || { echo "no mediaAssetId for $f: $out"; exit 1; }
```

**Storage is capped at 1 GB on the free tier** (`src/lib/storage-limits.ts`), with
30-day retention. Video is what fills it. Before a large batch, check headroom
with `postq media list --json` and clear superseded assets with `postq media
delete <id> --yes` (add `--force` only when the attached posts are cancelled).

Create the draft using JSON stdin, not command-line caption flags.

**Keep the fields separate.** `title` is PostQ's internal queue label: use something
human for the queue UI, never the folder slug. `platformTitle` is the short, platform-
facing title emitted by Content Factory (TikTok photo posts cap it at 90 runes).
`caption` is the full reviewed description. On TikTok video inbox drafts none of these
metadata fields can carry the caption; the creator pastes it in TikTok. For TikTok
photo posts, `platformTitle` becomes the title and `caption` remains the full
description.

```bash
printf '%s\n' '{
  "title": "Walkmon pet reveal",
  "platformTitle": "Your pet evolved",
  "caption": "Caption text\n\n#hashtags",
  "mediaAssetIds": ["<mediaAssetId>"]
}' | pnpm --silent postq -- posts create --from - --json
```

Keep the set name out of PostQ entirely; Content Factory's `status.json` already records
which set a post came from, via the handoff refs.

**A TikTok video draft cannot carry a caption at all.** TikTok's inbox endpoint
(`/v2/post/publish/inbox/video/init/`) accepts `source_info` only — it has no caption
field — so PostQ sends none and TikTok shows its own `#PostQueue` prefill instead. This
is TikTok's design: the inbox path is audit-exempt precisely because the creator writes
the caption in the app. Always hand the user the parsed caption verbatim to paste, and
tell them to delete TikTok's `#PostQueue` prefill. Deleting a platform prefill is not a
copy edit; do not take it as licence to reword the caption or swap in different
hashtags. See "Copy is transported, not authored" below. Photo slideshow drafts are the
exception,
`/v2/post/publish/content/init/` does accept title and description in `MEDIA_UPLOAD`
mode. Direct delivery publishes the caption automatically but needs `video.publish`, and
until the direct-post audit passes it forces `SELF_ONLY`.

**Queued posts are immutable.** `posts update` returns `validation_failed: Only draft posts
can be edited`, and cancelling moves the post to `canceled` rather than back to `draft`, so it
still cannot be edited. To change a scheduled post: `posts cancel`, then `posts create` a new
one, then schedule that, then re-run `mark-handoff --force` with the new post id.

Draft writes are allowed once the Content Factory output is approved. Do not schedule yet. Report:

- Content Factory output folder
- media asset id
- PostQ post id
- parsed caption
- on-video text blocks
- selected TikTok account candidate
- selected Instagram account candidate

## Schedule After Approval

**Content Factory approval is the approval.** A set whose `status.json` has
`review.state: "approved"` has been signed off by the user in the dashboard.
Schedule it into its goal slot without stopping to re-confirm the account or the
timestamp: the account follows from the set's `app`, and the time comes from
`configs/posting-goals.json`. Corrected 2026-08-10 after this extra gate left
approved batches unscheduled for days.

Stop only for something genuinely undetermined: a set with no matching goal
slot, inventory running out mid-week, or a delivery mode the goals do not
specify.

**Every scheduled post carries two targets on one slot.** TikTok as an inbox
draft (`format: "post"`, `tiktokDeliveryMode: "draft"`) and Instagram alongside
it at the same scheduled time. **The Instagram format depends on the media, and
so does the media itself:**

| Content | TikTok target | Instagram target | IG media |
|---|---|---|---|
| Walkmon video | `format: "post"`, draft | `format: "reel"` | the same MP4 |
| GainsLog / PlateSnap slides | `format: "post"`, draft | `format: "feed"` | the **4:5 variant**, not the 9:16 slides |

**Slideshows are not reels.** A TikTok photo slideshow's Instagram equivalent is
a feed carousel, so the IG target is `format: "feed"`. A reel target with image
media is rejected outright by the publisher, and quietly retargeting it to
`feed` with the 9:16 slides is what caused the 2026-08-17 incident.

**Do not reuse one media upload across both targets for slideshows.** Instagram's
feed refuses anything below 4:5 and pillarboxes it with white bars, so the 9:16
slides that are correct on TikTok render bar-framed on IG. `generate` writes a
4:5 variant to `output/<set>/instagram/slide_NN.png` for exactly this. Upload
both sets, then attach the IG variant to the IG target only, with
`payload.mediaAssetIdsOverride`:

```json
{
  "accountId": "<instagramAccountId>",
  "provider": "instagram",
  "format": "feed",
  "scheduledFor": "2026-06-26T08:00:00Z",
  "payload": { "mediaAssetIdsOverride": ["<ig-4x5-asset-id>", "..."] }
}
```

The override is ordered, so upload the IG slides in slide order. Without it the
target falls back to the post's base media, which is the 9:16 set. Walkmon
videos need no override: one MP4 serves both targets.

Validate payload shape with `--dry-run` when useful:

```bash
printf '%s\n' '{
  "targets": [
    {
      "accountId": "<tiktokAccountId>",
      "provider": "tiktok",
      "format": "post",
      "scheduledFor": "2026-06-26T08:00:00Z",
      "payload": { "tiktokDeliveryMode": "draft" }
    },
    {
      "accountId": "<instagramAccountId>",
      "provider": "instagram",
      "format": "reel",
      "scheduledFor": "2026-06-26T08:00:00Z",
      "payload": {}
    }
  ]
}' | pnpm --silent postq -- posts schedule <postId> --from - --dry-run --yes --json
```

Run the real schedule only after approval:

```bash
printf '%s\n' '{
  "targets": [
    {
      "accountId": "<tiktokAccountId>",
      "provider": "tiktok",
      "format": "post",
      "scheduledFor": "2026-06-26T08:00:00Z",
      "payload": { "tiktokDeliveryMode": "draft" }
    },
    {
      "accountId": "<instagramAccountId>",
      "provider": "instagram",
      "format": "reel",
      "scheduledFor": "2026-06-26T08:00:00Z",
      "payload": {}
    }
  ]
}' | pnpm --silent postq -- posts schedule <postId> --from - --yes --json
```

Important: do **not** set `manual: true` for TikTok inbox drafts. In PostQ, manual targets do not get `nextAttemptAt`, so the scheduler will not upload the draft to TikTok. TikTok inbox draft delivery is a normal scheduled target with `payload.tiktokDeliveryMode: "draft"`.

**Instagram target specifics.** Instagram publishes directly and carries the
caption from the PostQ draft automatically (the IG Graph API has no draft
state), so there is no caption-paste step on IG. If an IG target fails
validation, fix the media at the source and re-approve; do not drop the IG
target to make the TikTok side ship, and do not switch format to dodge the
error.

**Nothing manual survives the IG half.** TikTok delivery is an inbox draft that
gets finished by hand in the app, so any step left to that moment — picking a
sound, resizing, adjusting a cover — simply does not happen on Instagram, which
publishes straight from the API. Both 2026-08-17 failures were this same
mistake: the 4:5 sizing and the trending audio were TikTok-time manual steps,
mirrored to a surface that has no manual step. **When adding anything to the
TikTok flow, ask what the IG half does without a human present.**

Two known consequences of that, both by construction:

- **IG feed carousels are silent.** The Graph API cannot attach audio to a
  carousel. A slideshow on IG has no sound, and no payload field changes it.
- **Walkmon MP4s are rendered silent on purpose** (`-an` in `src/lib/video.ts`)
  so a trending sound can be chosen in the TikTok app. That leaves IG reels
  silent unless the IG variant is rendered with an audio bed mixed in.

### Night slots publish directly, and only night slots

Content Factory declares a daily cadence in `configs/posting-goals.json`: for
Walkmon and GainsLog on TikTok, **three `draft` slots (08:30 / 13:30 / 19:30)
and two `direct` slots (01:00 / 04:00), Europe/Stockholm**.

The two night slots exist because a draft has to be finished by hand in the
TikTok app, and nobody is awake at 01:00 to do it. They are a deliberate,
recorded exception to the default above, agreed with Ossian on 2026-08-10 and
written up as Rule 3l in Content Factory's `AGENTS.md`. **Do not widen it.** A
slot inside the waking day is a draft; only 01:00 and 04:00 are direct.

This TikTok-specific rule does not apply to Instagram. IG always publishes
directly (the Graph API has no inbox-draft state), so the daytime IG targets on
the same posts publish by construction, whatever their format.
The night-slot section below governs the TikTok half of the post only.

```bash
printf '%s\n' '{
  "targets": [
    {
      "accountId": "<tiktokAccountId>",
      "provider": "tiktok",
      "format": "post",
      "scheduledFor": "2026-08-11T23:00:00Z",
      "payload": {
        "tiktokDeliveryMode": "direct",
        "tiktokPrivacyLevel": "PUBLIC_TO_EVERYONE"
      }
    }
  ]
}' | pnpm --silent postq -- posts schedule <postId> --from - --dry-run --yes --json
```

Four things to get right:

- **`scheduledFor` is UTC, the goal is local.** 01:00 Stockholm is `23:00Z` the
  *previous* day in summer and `00:00Z` the same day from late October. Do not
  hand-convert: run `content-factory coverage --json` and read the missing
  slot's `at`, which is already resolved for the correct date.
- **Privacy must be `PUBLIC_TO_EVERYONE`.** The PostQ default is `SELF_ONLY`,
  which publishes privately and still needs a human to toggle it, defeating the
  entire purpose of a night slot.
- **The caption ships with a direct post**, unlike a draft. The
  `TIKTOK_DRAFT_CAPTION_WARNING` does not apply, so the caption in `post.md` is
  what actually goes live. Read it before scheduling; there is no native edit
  step to fix it afterwards.
- **Tag the experiment** so the reach cost of direct publishing is measured
  rather than assumed:

  ```json
  "experiment": { "id": "delivery-mode-001", "dimension": "delivery-mode",
    "variant": "direct-public",
    "hypothesis": "Direct-published night posts reach fewer viewers than inbox drafts finished by hand. Baseline is the draft slots on the same account in the same week." }
  ```

After scheduling a direct slot, record it locally so the mode is recoverable.
PostQ's `scheduled-posts` API does **not** return the delivery mode, so this
handoff record is the only place it is written down:

```bash
content-factory mark-handoff -s <set> -p tiktok --target postq \
  --scheduled-for <utc> --ref postId=<id> --ref deliveryMode=direct
```

`posts schedule` returns a `warnings` array and mirrors it to stderr. A captioned video
draft always warns that TikTok cannot receive the caption. Pass every warning through to
the user verbatim rather than swallowing it.

## Repair, Replace, Retry

Scheduling is not the end of the bridge. A queued post can need replacing
(the render was wrong) or retrying (the upload failed). All of these mutate
user data, so the same approval rule applies as for scheduling.

```bash
pnpm --silent postq -- posts cancel <postId> --yes            # withdraw a queued post
pnpm --silent postq -- posts reschedule <postId> --at <iso> --yes
pnpm --silent postq -- targets retry <targetId> --yes         # one failed target
pnpm --silent postq -- targets retry-failed --yes             # every failed target
pnpm --silent postq -- targets reschedule <targetId> --at <iso> --yes
pnpm --silent postq -- targets cancel <targetId> --yes
```

**Retry only after the cause is fixed and deployed.** `targets retry-failed`
re-runs everything that failed, so against an unfixed fault it reproduces the
same failure across every target at once. Read `failureReason` first, decide
whether it is transient (a token, a timeout) or structural (a payload the
platform rejects), and only retry the transient kind.

**Re-rendering media does not reach PostQ.** PostQ holds its own uploaded copy
from `media upload`. Re-running `generate-video` in Content Factory changes the
local file and nothing downstream, so a queued post keeps shipping the old
asset. To actually replace it: `posts cancel`, `media upload` the new file,
`posts create`, `posts schedule`, then re-record the handoff with the new ids.
Content Factory clears the handoff block on re-render precisely so this
divergence is visible rather than silent, which means the local record will say
"pending" while PostQ still has the old post queued until you reconcile.

**`mark-handoff` now refuses unapproved work.** A set whose `review.state` is
not `"approved"` (including the `pending` a re-render leaves behind) is rejected
with a hard error; recording a handoff requires either an approved verdict or an
explicit `--force`. This closes the gap where a handoff re-recorded after a
re-render shipped work nobody had re-approved. Do not use `--force` to paper
over a skipped review: if a re-render cleared the verdict, re-approve the new
asset in the dashboard before re-recording the handoff. Reconciliation of a
PostQ queue entry against a re-rendered set therefore goes: re-render →
re-approve in the dashboard → `posts cancel`/`create`/`schedule` → re-record
the handoff with `mark-handoff` (no `--force` needed once it is approved).

## Record The Handoff

Immediately after `posts schedule` returns `scheduled: true`, record it in
Content Factory so the set stops looking idle and cannot be handed over twice.
A dual-target post is recorded **once per platform**, sharing the same post id:

```bash
npx tsx src/cli.ts mark-handoff -s <set> -p tiktok --target postq \
  --scheduled-for <the same ISO timestamp you just scheduled> \
  --ref postId=<postId> \
  --ref mediaAssetId=<mediaAssetId> \
  --ref accountId=<tiktokAccountId> \
  --ref accountUsername=<tiktokUsername>

npx tsx src/cli.ts mark-handoff -s <set> -p instagram --target postq \
  --scheduled-for <the same ISO timestamp> \
  --ref postId=<postId> \
  --ref mediaAssetId=<mediaAssetId> \
  --ref accountId=<instagramAccountId> \
  --ref accountUsername=<instagramUsername>
```

When you hand the user a file to upload by hand instead of scheduling it, record
that too, so it gets the same duplicate protection and dedup treatment:

```bash
npx tsx src/cli.ts mark-handoff -s <set> -p tiktok --target manual \
  --note "handed to user for same-day manual upload"
```

This is not `mark-posted`. It records queued work, and leaves the set unposted.

## Status Honesty

Do not run `content-factory mark-posted` after draft creation or after scheduling. The Content Factory set is only posted when the user completes the post inside TikTok or explicitly confirms completion.

After confirmed native publishing, mark each platform it actually reached. A dual-target post needs two calls when both went live:

```bash
npx tsx src/cli.ts mark-posted -s <set> -p tiktok --app walkmon
npx tsx src/cli.ts mark-posted -s <set> -p instagram --app walkmon
```

`mark-posted -p tiktok,instagram` marks both at once when they went live together. Marking posted retires the matching handoff automatically, so there is nothing extra to clean up.

## Final Summary

Always include:

- Content Factory set path.
- PostQ media asset id (single upload, served to both targets).
- PostQ post id.
- Both accounts: TikTok id/username and Instagram id/username.
- Scheduled time and timezone (same slot for both targets).
- Delivery: TikTok `tiktokDeliveryMode: "draft"` (except the 01:00 and 04:00 night slots, `"direct"` with `tiktokPrivacyLevel: "PUBLIC_TO_EVERYONE"`; see "Night slots publish directly"), and the Instagram format (`reel` for video, `feed` for slides) publishing directly.
- The caption in full, flagged as something the user must paste in TikTok because a video draft cannot carry it, along with the `#PostQueue` prefill they need to replace. On Instagram the caption is already attached by the API, so no IG caption work is needed.
- On-video text blocks, labelled either "already baked into the MP4" or "still to add natively".
- The `review.state` that authorised the handoff, and who set it.
- That both handoffs were recorded with `mark-handoff`, and that the set is still unposted.
- Whether Content Factory `status.json` remains pending or was marked posted after confirmation.

## Verification

When editing this skill or helper, run from `ossian-stack`:

```bash
node --test skills/postq-bridge/scripts/parse-content-factory-post.test.mjs
python3 - <<'PY'
from pathlib import Path
import yaml
body = Path("skills/postq-bridge/SKILL.md").read_text()
front = body.split("---", 2)[1]
yaml.safe_load(front)
PY
scripts/skills-audit.py scan
```

When using the bridge, PostQ read-context smoke checks are safe. Media upload, draft creation, and real scheduling mutate user data; schedule only after explicit approval.
