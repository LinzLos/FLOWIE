# Expected finding — Case 004

FLOWIE should surface a **label-parity violation** on two of the three tabs:

> The tab labeled **"Billing"** targets a section headed **"Payments"**, and the
> tab labeled **"Team"** targets a section headed **"Members"**. The label on a
> control must match the heading of what it targets. A user who clicks
> "Billing" lands on a page that says "Payments" and scans for the word they
> clicked — and doubts they're in the right place. Screen-reader users hear one
> name in the tab list and a different name announced as the section heading.
> Rename one side of each pair so control and target agree ("Security" already
> does).

## Must include (to score "caught")

- Names **both** mismatched pairs (Billing → Payments, Team → Members) as
  control-label ≠ target-heading defects — not just "naming could be more
  consistent."
- States the user-facing consequence (clicked word isn't on the destination;
  assistive tech announces a different name).

## Score "partial" if

- It flags only one of the two pairs, or gestures at "inconsistent terminology"
  without pairing each control label with its target heading.

## Score "missed" if

- It critiques layout/heuristics and never compares tab labels against the
  headings they target.

## Invariant this case defends

```
label-parity: the label on a control must match the heading/title of its target
```

Designed trap (not a field miss): the input is code, so the divergence must be
*extracted* — the mismatch is never stated. "Security" matches on purpose, as
the control pair that should NOT be flagged.
