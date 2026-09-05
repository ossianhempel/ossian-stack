# Oversized And Parallel

Read for a large bundle or parallel focused validation. Follow the scope and safety contract in the skill entry point.
In commands and code examples, resolve bundled paths from the directory containing the loaded SKILL.md; do not use the caller's working directory.

## Oversized Bundles

The helper scans the full patch before partitioning it. A safe bundle that fits
the aggregate prompt limit remains one integrated review pass. Larger bundles
are split at bundle sections and file boundaries where possible; an oversized
single-file block is split at line boundaries with repeated file/hunk context
and an absolute new- or old-file line offset. Untracked snapshots use
injection-safe source-line records so continuation passes retain reportable
locations. A single physical diff line split across passes also retains its
original addition, deletion, or context marker.
Every original bundle byte appears exactly once across the pass sequence, and
all validated reports are merged before required-finding and exit-status checks.
The helper caps one run at eight bounded passes so an unexpectedly huge branch
cannot create unbounded model calls; split still-larger work into coherent review
targets.

Chunking makes large-diff review usable, but it cannot give one model call every
cross-file implementation detail. For architecture-heavy changes, still prefer
a coherent branch or PR shape whose semantic decision surface fits one pass.
Removing verified non-authoritative generated noise remains useful, but never
drop lockfiles, generated clients, policies, manifests, schemas, or other
independently semantic artifacts merely to shrink the review.
## Parallel Closeout

Format first if formatting can change line locations. Then it is OK to run tests and review in parallel:

```bash
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/autoreview" --parallel-tests "<focused test command>"
```

On Windows, the default `--parallel-tests` shell preserves the platform `cmd.exe`
semantics used by Python `shell=True`. Use `--parallel-tests-shell powershell`
or `--parallel-tests-shell pwsh` when the focused test command is PowerShell-specific.
Parallel tests inherit only a small allowlist of ordinary OS, CI, and toolchain
variables. Put additional non-secret project controls directly in the test command.
Home and standard config directories point to a temporary isolated root that is
removed after the command exits. Do not put secrets in the command because it is
printed before execution. Set `OPENCLAW_TESTBOX=1` on the autoreview process, not
inside the test command, because the environment snapshot and credential staging
happen before the test shell starts:

```bash
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
OPENCLAW_TESTBOX=1 "$SKILL_DIR/scripts/autoreview" --parallel-tests "pnpm check:changed"
```

On POSIX, the helper puts this isolated Testbox home under the short, sticky
system `/tmp`; Blacksmith creates an SSH control socket below that home, and a
long macOS `TMPDIR` can exceed the Unix-socket path limit. With an older helper,
prefix the outer autoreview process with `TMPDIR=/tmp`. Setting `TMPDIR` inside
the quoted test command is too late because the isolated home already exists.

This is the narrow trusted-maintainer-code exception: it stages only the Blacksmith
credential file into the temporary home so the command can delegate remotely. Never
use this credential-hydrated path for untrusted contributor or fork code. Run other
secret-bearing or credentialed tests separately in an appropriately isolated remote
runner.

Tradeoff: tests may force code changes that stale the review. If tests or review lead to code edits, rerun the affected tests and rerun review until no accepted/actionable findings remain. Once that rerun exits cleanly, stop; do not spend another long review cycle on redundant confirmation.
