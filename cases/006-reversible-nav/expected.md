# Expected finding — Case 006

FLOWIE should surface a **reversible-nav violation** on the advanced view:

> "Advanced delivery rules" is a one-way door. Clicking it hides the main view,
> and the advanced view offers **no back, close, or cancel** — its only control
> is "Apply rules", which **commits** the changes. A user who opens it just to
> look must either apply rules they didn't want or reload the page, which also
> discards any unsaved checkbox edits waiting in the main form. A path in must
> have a path out that returns to the prior state without loss. Add a
> back/cancel control to the advanced view that restores the main view with its
> pending edits intact.

## Must include (to score "caught")

- Identifies the advanced view as having **no exit besides commit** (the
  missing back/close/cancel on a one-way transition) — not just "navigation
  could be clearer."
- States the user-facing consequence: trapped into applying, or losing unsaved
  main-form edits via reload.

## Score "partial" if

- It suggests "add a back button" as generic polish, or cites easy-reversal as
  a heuristic, without identifying that this specific transition hides the
  prior view and offers commit as the only way out.

## Score "missed" if

- It reviews the forms and layout without tracing what happens after
  "Advanced delivery rules" is clicked.

## Invariant this case defends

```
reversible-nav: a path in must have a path out that returns to the prior state without loss
```

Designed trap (not a field miss): the input is code; the trap only appears by
tracing the interaction (click → view swap → what controls remain), not from
the resting layout, where both views' markup looks complete.
