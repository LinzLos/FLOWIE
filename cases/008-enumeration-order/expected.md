# Expected finding — Case 008

FLOWIE should surface **two order defects** on the same page, and leave the
third, correctly-ordered pair alone.

## 1 · Enumeration-order violation (heading ≠ rendered order)

> The section headed **"Inflow vs. Outflow"** renders its legend in the
> opposite order: **Outflow, Inflow, Target pace**. A label that enumerates
> items commits to their order; the eye follows the heading, then has to
> re-map it against the legend directly beneath it. Reorder the legend to
> Inflow, Outflow, Target pace — or rename the heading. One or the other, not
> both orders on one card.

## 2 · Operand-order violation (display order ≠ formula order)

> The Net Flow card states its own formula — **"Net flow = inflow − outflow"** —
> then renders the operands **Outflow 212** on the left and **Inflow 228** on
> the right. Read left to right, the card says `212 − 228 = −16`, which
> contradicts the **+16** printed directly above it. The reader either lands on
> the wrong sign or has to jump right-then-left to repair the order. Put Inflow
> first so reading order equals operation order: `228 − 212 = +16`.

## 3 · Must NOT be flagged (the control pair)

> **"Received vs. Cleared by specialist"** enumerates Received then Cleared,
> and the table columns render Received then Cleared, with a Net column equal
> to `received − cleared` on every row. Heading order, column order, and
> formula order all agree. Flagging this is a false positive.

## Must include (to score "caught")

- Names the **"Inflow vs. Outflow" heading vs. Outflow-first legend** mismatch
  as an ordering defect — not merely "the legend could be clearer."
- Names the **Net Flow operand order** defect *and proves it arithmetically*:
  left-to-right reading yields −16 against a displayed +16.
- Leaves the Received/Cleared table unflagged.

## Score "partial" if

- It finds only one of the two defects.
- It flags the operand order but treats it as taste ("consider leading with
  inflow") without showing the sign contradiction.
- It correctly flags both but also flags the Received/Cleared table.

## Score "missed" if

- It reads the numbers as merely inconsistent, critiques spacing/typography, or
  never compares any stated order against a rendered order.

## Invariant this case defends

Two invariants, **both registered in v2.9**. Neither was covered by the v2.8
set: `indexed-order` is the closest, but it is scoped to controls that index an
ordered set (nav, TOC, breadcrumb, tab strip, stepper) — a prose heading naming
two series is not a control, and the Net Flow card has no "control side" at all.

As shipped in `scripts/versions/v2.9/`:

```xml
<invariant name="enumeration-order" applies-to="heading, legend, caption, summary sentence, column-header group">
      Text that enumerates items commits to their order. Any label naming two or more things ("Inflow vs. Outflow", "Received and Cleared", "Name, Role, Status") must be rendered in the order it names them. This is the prose sibling of indexed-order: same failure, but the control side is a sentence rather than a nav. Check it by reading the label's order out as a list and comparing it to DOM/visual order — no domain knowledge required, so a mismatch is a fact rather than a preference.
    </invariant>

<invariant name="operand-order" applies-to="derived value shown beside its inputs — net, delta, difference, remaining, variance, subtotal">
      When a screen shows a derived value together with the operands it is computed from, the operands must read in the same order as the operation. net = in − out ⇒ In precedes Out. Reading order that contradicts operation order makes the reader either invert the sign or backtrack to repair it. Prove it arithmetically: compute the derivation in rendered order and compare it to the printed result — a sign flip or wrong magnitude is evidence, not opinion. Needs the formula; when it is neither stated on the surface nor inferable from the labels, skip rather than guess.
    </invariant>
```

`enumeration-order` is the mechanical one — a text-order vs. DOM-order
comparison with no domain knowledge and effectively no false-positive surface.
`operand-order` needs the formula, which is often stated on the card (as here)
or inferable from the label; when it isn't, skip rather than guess.

**Field-motivated designed trap** — a hybrid of 003 (field) and 004–006
(designed). The defect is real (see Provenance) but was rebuilt as a code
fixture rather than captured as-is, so both divergences must be *extracted* —
neither is named. The Received/Cleared table is the deliberate non-flag pair,
mirroring the role "Security" plays in 004.

## Provenance

Motivated by a field change in the `shift-prototype` loan-ops console
(2026-08-09): Overview queue cards shipped Outflow-left/Inflow-right while the
product's own copy, its Net Flow sub-label (`+203 in · -91 out`), and the Queue
Monitor section heading ("Inflow vs. Outflow") all named inflow first — and the
legend under that very heading rendered Outflow first. Fixed by flipping every
presentation surface to inflow-first; this case defends against the regression
and generalizes the rule beyond that one product.
