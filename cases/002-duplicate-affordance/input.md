# Case 002 — Duplicate affordance (one transition, three controls)

**Source:** "Attestation Shield" card in the NEAR AI / IronClaw Agent Monitor
concept prototype (built on the Tiny Wire design system).
**Type:** code + screenshot (the real prototype under test).

## The screen

A card that shows an agent's hardware attestation in two views:

- **Legible** view — a plain-language "Verified enclave" verdict plus a few facts.
- **Raw proof** view — the underlying TEE attestation quote.

A **segmented control** in the card header switches between the two views
(`Legible` / `Raw proof`).

## What was built

In addition to the segmented control, the card also had:

- An inline link at the bottom of the Legible view: **"Show the cryptographic proof →"**
  (switches to Raw proof — same as the segmented control's "Raw proof").
- An inline link at the bottom of the Raw proof view: **"← Back to the Shield"**
  (switches to Legible — same as the segmented control's "Legible").

So the single `legible ↔ raw` transition is driven by **three** controls: the
segmented control plus two inline links that duplicate it.

## The result

Two competing patterns for one action. The segmented control reads as the
canonical mode switch; the inline links are a second, redundant affordance for
the identical transition. It adds visual clutter, doubles what must be
maintained, and muddies which control is "the" control — without adding a new
capability.

## Why FLOWIE missed it (v2.6)

Every v2.6 coupling check models `control → target` and asks whether each
control is *consistent with* and *has an effect on* its target. All three
controls pass: each one works, each one reverses cleanly, labels are fine. The
defect isn't any single control — it's the **multiplicity**: more than one
control bound to the same transition. v2.6 never built the inverse
(`transition → controls`) map, so nothing could fire. Worse, the v2.6
`<compare>` step praised the screen's *consistency* without noticing the card
mixed a segmented control with inline links for one action.
