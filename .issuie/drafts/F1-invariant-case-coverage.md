## Description
Add a regression case for each v2.6 invariant that currently has no trap: `label-parity`, `count-parity`, `control-has-effect`, `reversible-nav` (cases 002–005). Today only `indexed-order` (case 001) is covered.

## Why
The invariant library is the core of v2.6's coupling checks, but 4 of 5 invariants ship untested — a fix could silently stop firing and no case would catch it.

## Scope
Test fixtures only. One folder per invariant, matching the existing `input.* / expected.md` format; add scoring-log rows.

## Touches
- cases/002-label-parity/, cases/003-count-parity/, cases/004-control-has-effect/, cases/005-reversible-nav/
- cases/README.md (scoring log)

## Source
v2.6 review: `<invariants>` lists 5; `cases/` has 1.

## Owner
Lindsay.

## Acceptance criteria
- [ ] A designed-trap case for each of the 4 uncovered invariants
- [ ] Each `expected.md` names the specific defect + caught/partial/missed bar
- [ ] Scoring-log rows added
