# Expected finding — Case 002

FLOWIE should surface a **duplicate-affordance / affordance-multiplicity
problem**: one state transition is driven by more than one control, roughly:

> The `legible ↔ raw` transition on the Attestation Shield is triggered by three
> controls — the segmented control (Legible / Raw proof) plus two inline links
> ("Show the cryptographic proof →" and "← Back to the Shield") that do the same
> thing. A transition should have one canonical control. Consolidate to the
> segmented control (it matches the Activity card's Intent / Raw logs pattern)
> and remove the duplicate links — unless a link is being kept as a deliberate,
> documented accessibility affordance.

## Must include (to score "caught")

- Names that **one transition has multiple controls** (not "each control works").
- Identifies it as an **affordance-multiplicity / redundancy** problem found by
  the inverse `transition → controls` map, not a single-control nit.
- Recommends a **canonical control** and removal/justification of the rest.

## Score "partial" if

- It flags vague "clutter" or "too many buttons" without naming that the
  controls drive the *same* transition, or without picking a canonical one.

## Score "missed" if

- It evaluates each control on its own (works / reverses / labeled) and never
  connects that they share one transition. *(This is what v2.6 did.)*

## Invariant this case defends

```
single-affordance: |controls(transition)| === 1
```

For any state transition (mode toggle, view switch, show/hide disclosure),
exactly one canonical control should trigger it, unless redundancy is a
deliberate, documented accessibility choice. Build the inverse map
(transition → controls); a transition with 2+ triggers is the smell.
