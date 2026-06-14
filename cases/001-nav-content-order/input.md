# Case 001 — Nav order vs. content order

**Source:** Tanay Kothari prototype for the Tinyware Design System.
**Type:** prose description (a screenshot of the screen would normally be the
input; this is the captured account of the real prototype).

## The screen

A documentation-style layout:

- **Left:** a side navigation listing the section categories.
- **Right:** a long, scrolling content panel. Each nav item corresponds to a
  content section on the right. Clicking a nav item scrolls the panel to that
  section.

## What was changed

The section categories in the **side nav were alpha-sorted (A–Z)**.

## What was NOT changed

The **content sections on the right were left in their original source order.**
None of the sections logically implicated by the nav sort were reordered to
match.

## The result

The nav order and the scroll order no longer agree. Using the nav to move
through the page jumps around — clicking down the alphabetized nav sends you
backward and forward through the unsorted content. The reading/scroll
experience is disorienting for anyone navigating by the side nav.

## Why FLOWIE missed it (v2.5)

Every v2.5 analysis step evaluates a single surface in isolation. The nav is
fine on its own; the content is fine on its own. The defect lives in the
*relationship* between them — a coupling invariant (`nav.order` must mirror
`content.order`) that no v2.5 step checks.
