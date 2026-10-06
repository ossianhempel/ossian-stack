# writing-for-agents

Vendored from [mattpocock/skills](https://github.com/mattpocock/skills) (`skills/productivity/writing-for-agents`).

Reference for writing any document an agent consumes — a skill, an `AGENTS.md` /
`CLAUDE.md`, or a doc reached by a pointer — plus `SKILL-MECHANICS.md` for
skill-specific frontmatter, invocation, and router choices.

To update:

```bash
npx skills add mattpocock/skills -y --skill writing-for-agents
cp -R .agents/skills/writing-for-agents/* skills/writing-for-agents/
trash .agents/skills/writing-for-agents
```
