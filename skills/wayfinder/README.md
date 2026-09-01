# wayfinder

Adapted from
[`mattpocock/skills`](https://github.com/mattpocock/skills/tree/main/skills/engineering/wayfinder).

The destination, shared map, decision-ticket frontier, fog-of-war, and
one-ticket-per-session model remain upstream. This copy is adapted to the
ossian-stack runtime contract:

- project setup routes through `setup-ossian-stack`;
- tracker operations prefer native capabilities and carry portable body-field
  fallbacks;
- upstream sibling calls this plugin does not ship are expressed inline;
- `prototype` and `domain-modeling` resolve to siblings this plugin ships.

Refresh into the scratch skill root, then merge by hand:

```bash
npx skills add mattpocock/skills -y --skill wayfinder
# hand-merge .agents/skills/wayfinder into skills/wayfinder, then:
trash .agents/skills/wayfinder
```

Never overwrite this directory from upstream: the portability adaptations are
part of the shipped behavior.
