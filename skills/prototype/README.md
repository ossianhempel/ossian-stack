# prototype

Merged from two upstreams into one skill.

- [mattpocock/skills](https://github.com/mattpocock/skills)
  (`skills/engineering/prototype`) — the branch split and its two bundled shapes,
  `LOGIC.md` (a single shareable HTML file a non-developer can click through) and
  `UI.md` (several radically different variants on one route). Both ship verbatim.
- [cursor/plugins](https://github.com/cursor/plugins)
  (`pstack/skills/poteto-mode/playbooks/prototype.md`) — the workflow around them:
  scope the decision first, gather references when the space is open, put variants
  behind one switcher, verify by observing, present a recommendation.

The framing worth keeping from Cursor: this is the one place where the bias toward
the smallest change and the usual verification bar both **invert**. Speed over
polish; the rigor is in picking the right design cheaply, not in the code.

And from mattpocock, the rule most often skipped: capture the prototype as a
primary source when done — throwaway branch, pointer from wherever the work is
tracked, and the verdict recorded *with the question it settled*. Main keeps only
the decision.

## References resolved

| Upstream | Here |
| --- | --- |
| `exhaust-the-design-space` principle skill | `principle-exhaust-the-design-space` |
| the control skill, for driving the surface | `close-the-loop` |
| Laziness Protocol | stated inline; folded into `simplify-code`, not shipped standalone |
| `Feature` playbook, `architect` skill | dropped — the handoff is stated plainly instead |

To update:

```bash
npx skills add mattpocock/skills -y --skill prototype   # LOGIC.md / UI.md are verbatim
npx skills add cursor/plugins -y --skill poteto-mode    # then hand-merge playbooks/prototype.md
```
