# domain-modeling

Adapted from [mattpocock/skills](https://github.com/mattpocock/skills)
(`skills/engineering/domain-modeling`), including `ADR-FORMAT.md` and
`agents/openai.yaml`.

The *active* discipline of building a domain model: challenge terms against the
glossary, sharpen fuzzy language, stress-test relationships with concrete
scenarios, cross-reference claims against the code, and write terms down the
moment they resolve. Reading a glossary for vocabulary is not this skill; this is
for when you are changing the model.

Its ADR gate is worth the price of admission: offer one only when the decision is
hard to reverse, surprising without context, **and** the result of a real
trade-off. Any one missing, skip it.

## What changed

Upstream names the glossary `CONTEXT.md`. This plugin uses `GLOSSARY.md`, so all
21 references were converted, `CONTEXT-FORMAT.md` was renamed to
`GLOSSARY-FORMAT.md`, and the multi-context `CONTEXT-MAP.md` became
`GLOSSARY-MAP.md`. Upstream's own wording argues for the rename — it says the
file "is a glossary and nothing else."

Pairs with `principle-model-the-domain`, which is the write-time rule for
encoding a domain in a structure rather than scattered conditionals.

To update:

```bash
npx skills add mattpocock/skills -y --skill domain-modeling
# hand-merge; this copy renames CONTEXT.md throughout, never overwrite
```
