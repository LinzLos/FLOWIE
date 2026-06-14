# Expected finding — Case 001

FLOWIE should surface a **coupling / ordering mismatch between the side nav and
the scrolling content**, roughly:

> The side nav is sorted alphabetically (A–Z), but the content sections on the
> right are in their original source order. A side nav is an index into the
> content, so its order must mirror the order of the sections it links to.
> Because they diverge, navigating by the nav scrolls the page out of sequence
> — jumping backward and forward through the content — which is disorienting.
> Either reorder the content sections to match the alphabetized nav, or sort
> both by the same key.

## Must include (to score "caught")

- Names that the **nav order and content order disagree** (not just "nav looks
  fine" or "content looks fine").
- Identifies it as a **cross-component / coupling problem**, not a single-surface
  layout nit.
- Notes the **consequence**: navigating produces an out-of-order / jumpy scroll.

## Score "partial" if

- It flags a vague "consistency" or "cognitive load" concern without naming the
  nav↔content order divergence as the cause.

## Score "missed" if

- It critiques the nav and the content separately and never connects their
  ordering. *(This is what v2.5 did.)*

## Invariant this case defends

```
nav.order === content.order
```

For any control that indexes an ordered set (side nav, table of contents,
breadcrumb, tab strip), the control's order must match the target's order.
