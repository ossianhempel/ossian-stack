# prototype

Merged from two upstreams into one skill.

- [mattpocock/skills](https://github.com/mattpocock/skills)
  (`skills/engineering/prototype`), the branch split and its two bundled shapes,
  `LOGIC.md` (a single shareable HTML file a non-developer can click through) and
  `UI.md` (several radically different variants on one route). The closeout sections are adapted for local scope limits.
- [cursor/plugins](https://github.com/cursor/plugins)
  (`pstack/skills/poteto-mode/playbooks/prototype.md`), the workflow around them:
  scope the decision first, gather references when the space is open, put variants
  behind one switcher, verify by observing, present a recommendation.

The framing worth keeping from Cursor: this is the one place where the bias toward
the smallest change and the usual verification bar both **invert**. Speed over
polish; the rigor is in picking the right design cheaply, not in the code.

Record the question and verdict with the runnable artifact. Production changes,
branch delivery, and tracker updates follow the scope the user authorized.

## References resolved

| Upstream | Here |
| --- | --- |
| `exhaust-the-design-space` principle skill | `principle-exhaust-the-design-space` |
| the control skill, for driving the surface | Existing project tooling or direct observation |
| Laziness Protocol | stated inline; folded into `simplify-code`, not shipped standalone |
| `Feature` playbook, `architect` skill | dropped, the handoff is stated plainly instead |

To update:

```bash
npx skills add mattpocock/skills -y --skill prototype   # preserve local closeout rules in LOGIC.md and UI.md
npx skills add cursor/plugins -y --skill poteto-mode    # then hand-merge playbooks/prototype.md
```
