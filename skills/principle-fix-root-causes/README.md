# principle-fix-root-causes

Vendored verbatim from [cursor/plugins](https://github.com/cursor/plugins)
(`pstack/skills/principle-fix-root-causes`).

A debugging principle: trace each symptom to its root cause and fix it there.
`disable-model-invocation: true`, so it fires only when you invoke it.

It is kept as its own skill rather than folded into `simplify-code` because it
governs a different moment. `simplify-code` restructures code that already works
and explicitly is not a bug hunt; this one applies while you are chasing a
failure. The one piece that does transfer — a guard added to silence a crash is
a symptom fix, and fix the pattern rather than the instance — is stated in
`simplify-code` alongside rules 5 and 12.

To update:

```bash
npx skills add cursor/plugins -y --skill principle-fix-root-causes
cp -R .agents/skills/principle-fix-root-causes/. skills/principle-fix-root-causes/
```
