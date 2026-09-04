# resolve-pr-feedback

This copy uses a neutral name, generic orchestrator references, and bundled
helper scripts and documents so it can run as a self-contained plugin skill.

GitHub/GHE retains its full/targeted helpers. Azure DevOps Services dispatches to
`references/azure-devops.md` and the Python adapter under `scripts/azure/`. It
handles inline/general discussion, preserves deleted/system-comment distinctions,
and checks assessed head/thread evidence before replies or status changes. Both
providers use the same decision and pipeline residual contracts.

The Azure adapter uses REST 7.1 and existing az Entra authentication or a supplied
AZURE_DEVOPS_EXT_PAT. It does not support Server/custom hosts or fork mutations.
Thread writes have no atomic compare-and-swap guarantee; readback and reassessment
are required. Offline fixtures do not establish live access or write success.
The duplicated client.py in babysit must stay identical for skill isolation.

To update:

```bash
# Fetch the upstream source recorded in skills/sources.json, then hand-merge it
# into skills/resolve-pr-feedback/; this copy is renamed and adapted
```
