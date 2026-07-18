# Expected finding — Case 003

FLOWIE should surface a **control-has-effect violation / false affordance**:

> The "standing declaration" rule pills (`rank by · fit`, `sponsored bias · off`,
> `injected offers · → my queue`) are styled as interactive controls but trigger
> no observable change. A control must observably change its target; here the
> surface's *central governing object* presents several control affordances with
> no effect, while the only working control is one link at the bottom. Make at
> least one rule **live** — e.g., toggling `sponsored bias` re-ranks the list so
> the sponsored option rises — so the declaration *demonstrably* governs the
> decision. Or restyle the inert pills so they read as static state, not
> controls.

## Must include (to score "caught")

- Names that **elements styled as controls have no effect** (false affordance /
  control-has-effect) — not just "needs more interaction."
- Connects it to the surface's own claim (`governs this decision`) going
  **undemonstrated** because the controls that should prove it are dead.
- Recommends making a rule **live** (or restyling the inert ones as state).

## Score "partial" if

- It says the screen "feels static" or "could use a toggle" without naming that
  the existing declaration pills are **false affordances with no effect**.

## Score "missed" if

- It evaluates layout/heuristics and never flags that interactive-looking
  declaration controls do nothing.

## Invariant this case defends

```
control-has-effect: every control observably changes its target
```

…extended with an **affordance-honesty corollary**: an element styled as a
control MUST be a control. Anything that signals interactivity (chip / pill /
toggle treatment) and does nothing is a false affordance — either wire it or
restyle it as static state. Build the map `control → effect`; a styled control
with an empty effect set is the smell.
