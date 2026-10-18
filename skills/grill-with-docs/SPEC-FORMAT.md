# Spec Format

A spec turns a finished grilling session into the brief an implementer works
from — you in a later session, another agent, or a fresh subagent that inherits
nothing. Write it for that reader.

## Where it goes

Follow the project's existing spec or plan location if it has one. Otherwise
write `docs/specs/<slug>.md`, creating the directory when the first spec is
written. Update an existing spec for the same work instead of adding a second.

## Template

```md
# {Feature or change, in the project's GLOSSARY.md terms}

## Goal
{What a user or caller can do afterwards that they cannot do now. 1-3 sentences.}

## Decisions
- {Each decision the session settled, with the reason when it is not obvious.
  Link the ADR when one was written.}

## Out of scope
- {What was raised and deliberately left out.}

## Behavior
- {Observable behavior that proves the change works, one check per line:
  input or action → expected result on the surface the user touches. These
  become the first tests.}

## Build order
1. {The smallest unit that can be built and checked on its own, naming the
   behavior checks it satisfies.}
2. {The next unit, building on the first.}
```

## Rules

- **No tickets.** Work is split into the build order inside the spec, not into
  tracker issues. Each unit is small enough to build and verify in one pass and
  leaves the project working.
- **Behavior, not implementation.** Behavior checks state what is observed, not
  which functions exist, so they survive the implementer's choices.
- **Nothing open.** If writing a section exposes an unsettled decision, it is
  another grilling round, not a TODO in the spec.
- Keep it short. A section with nothing real to say is omitted.
