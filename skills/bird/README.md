# Bird

Adapted from OpenClaw's [Bird skill](https://github.com/openclaw/openclaw/blob/76b5208b11eebf2071ad5a363666467417ea5792/skills/bird/SKILL.md),
MIT, pinned to `76b5208b11eebf2071ad5a363666467417ea5792`.
Upstream later removed that skill in `31a7e4f9375f64ee3177bdc955cbe73dadfd96b1`.

Local changes: portable metadata, bounded reads, source attribution, explicit
account-action authorization, account consistency, credential protection,
write verification, and installed-command corrections. In particular, avoid
raw `bird check` because version 0.8.0 prints cookie prefixes. Codex UI metadata
is a local addition. The CLI package is not bundled with this skill.

Verified 2026-10-07: npm `@steipete/bird@0.8.0` runs on Node.js 24, but the
publisher marks it deprecated/unsupported. The public `steipete/bird` repository
and `steipete/tap/bird` formula are unavailable. A previously installed Homebrew
0.6.0 binary had an invalid signature; npm installation plus unlinking that old
formula restored the command. Recheck installation sources when updating.

Refresh by hand: retrieve the pinned upstream file with
`gh api 'repos/openclaw/openclaw/contents/skills/bird/SKILL.md?ref=76b5208b11eebf2071ad5a363666467417ea5792' -H 'Accept: application/vnd.github.raw+json'`,
then compare with local SKILL.md. Do not replace local behavior with the historical
copy. Confirm changed examples against `bird <command> --help`.
