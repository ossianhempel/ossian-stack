---
name: visual-parity
description: "Match a UI to a reference through controlled captures and image-diff evidence on the real surface."
---

# Visual Parity

Use when one UI must match another implementation, screenshot, design reference,
or pre-migration baseline. The reference is the contract unless the user changes
it.

## Establish comparable captures

1. Name the components, states, devices, locales, appearances, content, fonts,
scale, and viewport covered.
2. Capture the baseline before changing code. Preserve it outside generated build
output and record its provenance.
3. Capture the implementation under the same conditions. Normalize only transport
properties that do not affect appearance; never edit the baseline to reduce a diff.
4. Choose the pass rule. Pixel-zero is suitable for deterministic renderer-to-
renderer migrations. A user-approved tolerance or region mask is required for
antialiasing, timestamps, media, or platform-rendering differences.

## Converge

Change shared primitives first when several components depend on them. Then work
one component or state at a time. Produce an image diff and inspect the delta by
region. Change one likely cause, recapture, and repeat. Do not restructure product
code solely to game the capture harness.

Use the project's `verify-*` skill to launch, drive, and preserve evidence. Use the
relevant UI craft skill for implementation details. Separate independent component
work into isolated worktrees; serialize shared primitives.

If the reference itself is wrong or incomplete, stop that comparison and surface
the specific decision. Do not silently redefine parity.

## Reply

Report every component and state checked, capture conditions, baseline and result
paths, diff metric and threshold, remaining mismatches, and any regions excluded
with the user's reason.
