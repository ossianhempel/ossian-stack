# Engines And Panels

Read for an explicitly selected engine/model, override, or opt-in reviewer panel. Follow the scope and safety contract in the skill entry point.
In commands and code examples, resolve bundled paths from the directory containing the loaded SKILL.md; do not use the caller's working directory.

## Review Panels

Run multiple reviewers against one frozen bundle:

```bash
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/autoreview" --reviewers codex,claude,pi
```

`--panel` is shorthand for Codex plus Claude unless `--engine` changes the first reviewer:

```bash
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/autoreview" --panel
```

Set reviewer models and thinking/effort explicitly:

```bash
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/autoreview" --reviewers codex,claude --model codex=gpt-5.6-sol --thinking codex=high --model claude=claude-fable-5 --thinking claude=max
```

Inline syntax is also supported for simple model IDs:

```bash
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/autoreview" --reviewers codex:gpt-5.6-sol:high,claude:claude-fable-5:max
```

For models with slashes or extra colons, prefer keyed form:

```bash
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/autoreview" --engine pi --model anthropic/claude-sonnet-4 --thinking high
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/autoreview" --reviewers codex,pi --model codex=gpt-5.6-sol --model pi=anthropic/claude-sonnet-4
```

`--reviewers all` covers Codex, Claude, and Pi. Droid, Copilot, Cursor, and OpenCode selections fail closed because their current CLI contracts cannot confine project instructions, filesystem reads, or network fetches to the review boundary.
## Models and thinking

The helper accepts `--model` globally or per engine (`engine=model`) and `--thinking` globally or per engine (`engine=level`). Repeat either flag for multiple reviewers.

Recommended model defaults:

| Engine              | Default model                                      | Source note                                           |
| ------------------- | -------------------------------------------------- | ----------------------------------------------------- |
| **codex** (default) | `gpt-5.6-sol` -> `gpt-5.6-terra` on access failure | OpenClaw org review default                           |
| **claude**          | `claude-fable-5`                                   | Anthropic's most capable widely released Claude model |

CLI flags and environment variables override these defaults. Pi does not get a built-in model default because its provider catalog may vary by installation. Droid, Copilot, Cursor, and OpenCode are currently refused.

| Engine              | Model flag                 | Example model IDs                                                            | Thinking flag                 | Accepted levels                                            |
| ------------------- | -------------------------- | ---------------------------------------------------------------------------- | ----------------------------- | ---------------------------------------------------------- |
| **codex** (default) | `codex --model X exec ...` | `gpt-5.6-sol`, then `gpt-5.6-terra` on Sol access failure                    | `-c model_reasoning_effort=Y` | `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max` |
| **claude**          | `claude --model X`         | `claude-fable-5`, `claude-opus-4-8`, `claude-sonnet-4-6`, `claude-haiku-4-5` | `--effort Y`                  | `low`, `medium`, `high`, `xhigh`, `max`                    |
| **droid**           | currently refused          | Factory model IDs                                                            | `-r, --reasoning-effort Y`    | `off`, `none`, `low`, `medium`, `high`, `xhigh`, `max`     |
| **copilot**         | currently refused          | Copilot model aliases                                                        | not supported                 | n/a                                                        |
| **pi**              | `pi --model X`             | `anthropic/claude-sonnet-4`, `openai/gpt-4o`                                 | `--thinking Y`                | `off`, `minimal`, `low`, `medium`, `high`, `xhigh`         |
| **cursor**          | currently refused          | Cursor model aliases                                                         | not supported                 | n/a                                                        |
| **opencode**        | currently refused          | OpenCode provider/model IDs                                                  | not supported                 | n/a                                                        |

Claude also supports `--fallback-model a,b` for availability-based fallback chains ([model-config](https://code.claude.com/docs/en/model-config)). Current Claude docs note that auth, billing, rate-limit, request-size, and transport errors do not trigger fallback, and the changelog documents interactive-session support in `v2.1.166`.

[OpenAI's model guidance](https://developers.openai.com/api/docs/guides/latest-model) identifies Sol as the GPT-5.6 frontier-capability route and documents `max` support. Autoreview keeps `medium` as its default reasoning level to balance quality and usage; use `high` or `max` for the hardest quality-first reviews when the extra cost is worth it.

Examples matching current `main` behavior:

```bash
# Codex with explicit model and reasoning (defaults to medium)
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/autoreview" --engine codex --model gpt-5.6-sol --thinking medium

# Codex fast mode (priority service tier); needs a model whose catalog lists the tier, silently standard otherwise
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/autoreview" --engine codex --codex-speed fast

# Safe Codex model/response tuning overrides (--codex-speed wins over a service_tier here)
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/autoreview" --engine codex --codex-config 'service_tier="fast"'

# Claude Code aliases or full model names, with optional availability fallback
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/autoreview" --engine claude --model claude-fable-5 --thinking max
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/autoreview" --engine claude --model claude-fable-5 --fallback-model claude-opus-4-8,claude-sonnet-4-6

# Pi with explicit model and thinking level
SKILL_DIR="<absolute directory containing the loaded SKILL.md>";
"$SKILL_DIR/scripts/autoreview" --engine pi --model anthropic/claude-sonnet-4 --thinking high --pi-bin pi

```

`--cursor-agent-bin` and `CURSOR_AGENT_BIN` remain compatibility aliases for
`--cursor-bin` and `CURSOR_BIN`.

### Environment defaults

CLI flags take precedence over environment variables.

Store persistent personal defaults in your shell startup file or launcher
environment. For repository-local defaults, use an existing local environment
loader such as an untracked `.envrc`; the helper does not write a config file.

| Variable                           | Purpose                                                                                                                          |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `AUTOREVIEW_MODEL`                 | Override the built-in default `--model` for all engines                                                                          |
| `AUTOREVIEW_THINKING`              | Default `--thinking` for all engines                                                                                             |
| `AUTOREVIEW_FALLBACK_MODEL`        | Default Claude `--fallback-model` chain                                                                                          |
| `AUTOREVIEW_<ENGINE>_MODEL`        | Per-engine model override, for example `AUTOREVIEW_CODEX_MODEL=gpt-5.6-sol`                                                      |
| `AUTOREVIEW_<ENGINE>_THINKING`     | Per-engine thinking override                                                                                                     |
| `AUTOREVIEW_CODEX_CONFIG`          | Safe Codex model/response tuning overrides, semicolon-separated, e.g. `service_tier="fast"`; capability-bearing keys fail closed |
| `AUTOREVIEW_CODEX_SPEED`           | Codex service tier override: `fast` (priority), `flex`, or `default`; silently standard when the model does not list the tier    |
| `AUTOREVIEW_CLAUDE_FALLBACK_MODEL` | Claude-only fallback chain                                                                                                       |
| `AUTOREVIEW_PROVIDER_ENV_ALLOW`    | Comma-separated custom Pi/OpenCode credential variable names; names must end in a recognized credential suffix                   |

Codex maps thinking to `model_reasoning_effort`. Claude maps thinking to `--effort`. Pi maps thinking to `--thinking`. Only Claude accepts `--fallback-model`; global CLI/env fallback requires at least one Claude reviewer, and engine-specific fallback overrides require that reviewer to be selected. Non-Claude fallback overrides, including `AUTOREVIEW_<NONCLAUDE>_FALLBACK_MODEL`, fail closed instead of being silently ignored.
