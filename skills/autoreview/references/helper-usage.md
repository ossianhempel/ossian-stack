# Helper Usage

Read for helper options, native Windows invocation, or harness verification. Follow the scope and safety contract in the skill entry point.
In commands and code examples, resolve bundled paths from the directory containing the loaded SKILL.md; do not use the caller's working directory.

## Helper

Resolve the loaded skill path in each command:

```bash
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/autoreview" --help
```

The smoke harness has thin shell wrappers over a shared Python implementation:

```bash
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/test-review-harness" --fixture benign --engine codex
```

On native Windows, invoke the extensionless Python helper through Python:

```powershell
$SkillDir = "<absolute directory containing the loaded SKILL.md>";
python (Join-Path $SkillDir "scripts/autoreview") --help
```

and the smoke harness:

```powershell
$SkillDir = "<absolute directory containing the loaded SKILL.md>";
& (Join-Path $SkillDir "scripts/test-review-harness.ps1") -Fixture benign -Engine codex
```

The helper:

- chooses dirty local changes first
- accepts `--mode uncommitted` as an alias for `--mode local`
- otherwise uses current PR base if `gh pr view` works
- otherwise uses `origin/main` for non-main branches
- does not fetch automatically during branch review; the selected base ref must already resolve locally
- recognizes `--engine droid`, `copilot`, `cursor`, and `opencode` only to fail closed with isolation errors; runnable engines are `codex`, `claude`, and `pi`; default is `AUTOREVIEW_ENGINE` or `codex`
- resolves bare `git`, `gh`, reviewer, and PowerShell shell commands from absolute `PATH` entries only, never from the reviewed checkout; explicit `--*-bin` paths are interpreted from the reviewed repository root when relative and accepted only when both the supplied path and resolved target stay outside the reviewed repository
- use `--mode commit --commit <ref>` for already-committed work, especially clean `main` after landing
- scans safe Git patches in full, recognizes synthetic fixture values tied to their credential field, reviews them in one pass up to the aggregate prompt limit, and automatically uses complete bounded passes above it
- should be left in `--mode auto` or forced to `--mode branch` for PR/branch work; do not force `--mode local` after committing
- writes only to stdout unless `--output`, `--json-output`, or live streamed engine stderr is set
- supports `--dry-run`, `--parallel-tests`, `--parallel-tests-shell`, `--prompt`, repo-relative `--prompt-file`, repo-relative `--dataset`, `--no-tools`, `--no-web-search`, repeatable Codex-only safe model/response tuning with `--codex-config key=value`, Codex-only `--codex-speed fast|flex|default`, and commit refs
- supports `--stream-engine-output` or `AUTOREVIEW_STREAM_ENGINE_OUTPUT=1` for live engine text while preserving structured validation; Codex and Claude hide tool/file event details, emit compact activity summaries, and report usage at turn completion
- supports opt-in review panels with `--panel` / `--reviewers`, plus per-engine `--model`, `--thinking`, and Claude `--fallback-model`
- uses built-in defaults `codex=gpt-5.6-sol` with `high` reasoning and an access-only `gpt-5.6-terra` retry, plus `claude=claude-fable-5`; honors `AUTOREVIEW_MODEL`, `AUTOREVIEW_THINKING`, `AUTOREVIEW_FALLBACK_MODEL`, and per-engine `AUTOREVIEW_<ENGINE>_MODEL` / `AUTOREVIEW_<ENGINE>_THINKING` environment overrides when CLI flags are omitted
- gives Codex the bundle in an empty workspace with web search available; Claude receives the bundle plus WebSearch by default and optional domain-constrained WebFetch, and Pi receives the bundle with no tools
- runs Claude with `--safe-mode` (`v2.1.169+`), `--setting-sources user`, MCP and auto-memory disabled, no filesystem/shell tools, an empty external workspace, and `--fallback-model` when set
- refuses Droid, Copilot, Cursor, and OpenCode reviews until their CLIs expose the required project, filesystem, and network isolation
- runs Pi `v0.79.0+` from neutral temporary directories with `--no-approve`, `--no-session`, disabled Pi context/resource loading, and `--no-tools` because its built-in read tools are not repository-confined
- prints `review still running: <engine> elapsed=<seconds>s pid=<pid>` to stderr at long-running intervals while waiting for the selected review engine, unless streamed output or compact Codex activity has been visible recently
- prints `autoreview clean: no accepted/actionable findings reported` when the selected review command exits 0
- exits nonzero when accepted/actionable findings are present
