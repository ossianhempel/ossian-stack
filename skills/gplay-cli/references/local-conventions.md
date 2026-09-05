# Ossian Stack conventions

## Discover the installed surface

Confirm commands and flags from the installed CLI before constructing a write:

```bash
gplay --help
gplay <command> --help
```

Prefer JSON output for inspection and automation. Use explicit long flags,
deterministic package and track selection, and pagination when completeness
matters. A missing `gplay` binary is a prerequisite problem, not permission to
fall back to browser automation without saying so.

## Credentials

Use the `one-password` skill whenever authentication material is needed. Prefer
`op run` or a short-lived file produced for the command over copying a Google
service-account JSON key into the repository. Keep credential files and `.env*`
files ignored, never print their contents, and remove temporary key files after
use.

Run `gplay auth doctor` before diagnosing API failures. Confirm the selected
Google account, developer account, package, and required Play Console grants;
authentication success alone does not prove authorization for the app.

## Mutation boundary

Read current state before changing it and preview with `--dry-run` when the
command supports it. Show the concrete package, track, version, rollout, locales,
products, users, or grants that will change.

Uploading to an internal or requested testing track is authorized by a direct
request to distribute that build. Publishing or promoting to production,
changing a live rollout, replying publicly to reviews, issuing refunds, changing
prices or product availability, and changing users or grants require authorization
for that concrete action in the current request or existing session context. Do
not ask again when that authorization is already present.

Google Play writes commonly use an edit transaction. Preserve its lifecycle:

1. Create the edit.
2. Apply all intended changes to that edit.
3. Validate the edit.
4. Commit only after the preview and authorization requirements are satisfied.

Do not leave an edit committed while describing the action as a dry run.

## Release evidence

After a mutation, read back the affected resource. For releases, verify the
target track, version code, release status, and staged rollout fraction. Separate
these states in the report:

- artifact built locally;
- artifact uploaded;
- release visible on a testing track;
- production rollout started or changed;
- rollout complete.

Treat Console-only declarations or policy forms as remaining work unless the API
response proves them complete.
