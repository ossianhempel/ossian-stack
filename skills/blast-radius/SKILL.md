---
name: blast-radius
description: "Find what a change could break beyond its diff and prove the safety assumptions that matter before delivery."
---

# Blast Radius

Audit a change for breakage that symbol search and local review can miss. This is
read-only unless the user also asked for fixes. Work from the diff, its base, and
the real consumers of changed behavior.

## Trace the change outward

1. Explain the behavior that changed, including persisted data, wire formats,
lifecycle timing, feature flags, generated artifacts, and callers in other
languages or services.
2. Use `how` to trace ownership and `why` when a historical constraint matters.
3. Identify the one or two facts on which safety depends. Prefer a small decisive
fact over a long speculative risk list.
4. Follow each fact past local symbol references: dependency source at the pinned
version, serializers and readers, scheduled work, external APIs, configuration,
and downstream state.

## Prove the safety facts

Take each important fact as far as the available evidence allows:

1. Source location.
2. A demonstrated path showing the bad case cannot reach the change.
3. A script or focused test that calls the shipped code.
4. Reproduction in the running product.

Prefer levels 3 or 4. Mark a fact `unproven` when it cannot be checked cheaply.
Do not add broad tests merely to make the audit look rigorous. A focused probe is
better when it exercises the real contract and can be removed after use.

Classify each remaining risk by mechanism, likelihood, impact, and the cheapest
check that would catch it. Separate confirmed risks from cases checked and
cleared. Do not edit product code unless the user's scope includes fixes.

## Reply

Report what changed, the safety facts and evidence level reached, confirmed risks,
cleared concerns, and the cheapest remaining pre-delivery check. Cite the source
and artifact paths used.
