## Description
Implement the role-based critique lenses the README advertises — navigator, friction-tester, accessibility — as selectable passes mapped onto FLOWIE's existing steps.

## Why
The README lists these "on the roadmap" and CHANGELOG 2.5 mentions a lightweight agent model, but the v2.6 script has no explicit role lenses. Closing the gap lets a user run a focused critique from one perspective.

## Recommended prerequisite
None (script change — serializes with F3/F4 on the v2.7 file).

## Scope
Add an optional lens selector that scopes the critique passes; reuse existing heuristic/coupling/interaction steps per lens. No new analysis engine.

## Touches
- scripts/versions/v2.7/* (shared — new version file)

## Source
README "On the roadmap: role-based critique lenses…"; CHANGELOG 2.5 agent model.

## Owner
Lindsay.

## Acceptance criteria
- [ ] navigator / friction-tester / accessibility lenses selectable
- [ ] each maps to existing passes, scoping the output
- [ ] default (no lens) behaviour unchanged
