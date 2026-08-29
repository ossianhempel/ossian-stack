# teach

Vendored from [cursor/plugins](https://github.com/cursor/plugins) (`pstack/skills/teach`).

Explains a change or subsystem plainly, at the person's pace. Sits on top of `how`
and `why`, running both and weaving their findings into one account, and writes
every response through `unslop`. Those three skills must stay installed alongside it.

Replaced the previous `teach` vendored from
[mattpocock/skills](https://github.com/mattpocock/skills), which was an unrelated
multi-session learning-workspace skill.

To update:

```bash
npx skills add cursor/plugins -y --skill teach
cp -R .agents/skills/teach/. skills/teach/
```
