# agents/openai.yaml Reference

`agents/openai.yaml` is Codex/ChatGPT skill metadata. It configures how a skill
is displayed in those UIs, whether Codex may invoke it implicitly, and which
tool dependencies it has. Claude Code and Cursor ignore it entirely.

Official documentation:
- Codex skills: https://developers.openai.com/codex/skills
- ChatGPT skill building: https://learn.chatgpt.com/docs/build-skills
- Note: the Agent Plugins 1.0 spec (agent-plugins.org) does NOT cover
  `agents/` — it is OpenAI client-specific, not part of the portable format.

## File format

```yaml
interface:
  display_name: "Resolve PR Feedback"          # shown instead of the kebab name
  short_description: "Address reviewer feedback on a PR commit by commit"
  icon_small: "./assets/small-logo.svg"        # optional
  icon_large: "./assets/large-logo.png"        # optional
  brand_color: "#3B82F6"                       # optional
  default_prompt: "Optional prompt wrapper"    # optional

policy:
  allow_implicit_invocation: false             # default true

dependencies:
  tools:
    - type: "mcp"
      value: "someServer"
      description: "What it is for"
      transport: "streamable_http"
      url: "https://example.com/mcp"
```

## Rules for this repo

1. **Every shipped skill has one.** A skill without the file displays in Codex
   as `Plugin Name: kebab-name` with the full SKILL.md description, which is
   inconsistent with the rest of the plugin.
2. **`short_description` is 25–64 characters.** Both ends are hard constraints
   (OpenAI's own generator enforces this range). Distill, don't copy.
3. **`display_name` is Title Case** of the kebab name with acronyms restored
   (ASC, CLI, iOS, PR, UI). OpenAI's generator logic is Title Case with a
   small-word/acronym list; match it rather than inventing a different style.
4. **Partial updates only.** When a file already exists, edit the field you
   need and leave `policy:` and `dependencies:` untouched — regenerating the
   file silently drops the invocation policy.
5. **Policy pairing.** `disable-model-invocation: true` in SKILL.md (Claude
   Code, Cursor) must be mirrored by `policy.allow_implicit_invocation: false`
   here (Codex reads only this file). The repo validator (`bun run validate`)
   fails on a one-sided declaration.
6. **Vendored skills.** Upstreams rarely ship this file; a local
   `agents/openai.yaml` is a local addition — record it in the skill's
   `sources.json` notes so a refresh doesn't silently treat the skill as
   unmodified upstream, and merge by hand.

## Checking your work

```bash
# short_description length (strip the key, quotes, and trailing newline)
sed -n 's/^  short_description: "\(.*\)"$/\1/p' skills/<name>/agents/openai.yaml | tr -d '\n' | wc -c

# repo-wide: manifest, policy pairing, README inventory
bun run validate
```
