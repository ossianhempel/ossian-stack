---
name: grill-with-docs
description: A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go and ends with a written spec.
disable-model-invocation: true
---

Load and follow `grilling` and `domain-modeling` using the host's installed-skill mechanism.

When the user confirms the shared understanding, write the spec before anything
is built: one file in the format of [SPEC-FORMAT.md](./SPEC-FORMAT.md). It is the
input to implementation, so it records every settled decision and leaves nothing
for the implementer to guess. Show the user the path and stop; building it is a
separate request.
