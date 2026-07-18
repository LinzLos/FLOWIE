# Case 003 — Dead controls (styled as interactive, wired to nothing)

**Source:** the "declarative trust surface" (the *fixed* state) in the
agentic-trust-devtools demo — a coding agent that surfaces a sponsored auth
recommendation under a user's standing declaration. Built on the Tiny Wire
design system.
**Type:** code (the real prototype under test).

## The screen

The fixed/declarative state leads with a **"standing declaration"** — three rule
pills that supposedly govern the decision:

- `rank by · fit`
- `sponsored bias · off`
- `injected offers · → my queue`

…with a `governs this decision ▼` arrow into a ranked list of auth options
(AuthForge chosen, Sessionly, Authora demoted + rerouted to a queue).

## What was built

All three declaration rules were rendered as **pills styled identically to the
interactive controls used elsewhere in the system** (rounded, bordered — the
same chip/toggle treatment). None were wired: clicking any did nothing. The
ranked list was static. The only working control on the entire surface was a
single "Offers queue" link at the very bottom.

So the surface's central object — the declaration that the UI claims *governs*
the ranking — presented several control affordances, none of which had any
effect.

## The result

The interface asserts that the declaration drives the decision (`governs this
decision ▼`), but nothing on screen demonstrates it. The rule pills are **false
affordances**: they look clickable, invite interaction, and do nothing. A user
(or a founder watching the demo) can't tell which elements are live, and the
core claim — "your declaration governs the ranking" — is *stated, never shown*.
Interactivity is concentrated in one bottom link, away from the surface's own
thesis.
