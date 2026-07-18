# FLOWIE Regression Cases

Each folder here is one **known failure mode** — a defect FLOWIE should catch.
Re-run these against any new version of the script to measure what it catches
and to make sure fixes don't backslide.

## Folder format

```
NNN-short-slug/
  input.*       The prototype under test (screenshot, code, or prose description).
  expected.md   What FLOWIE SHOULD surface for this input.
```

## How to run a case

1. Feed `input.*` to FLOWIE (the current version in `manifest.json`).
2. Compare FLOWIE's output against `expected.md`.
3. Score the result:
   - **caught** — FLOWIE surfaced the expected finding.
   - **partial** — it hinted at it but didn't name the real defect.
   - **missed** — it said nothing relevant.

## Scoring log

Track each version's hit rate as cases accumulate.

| Case | v2.5 | v2.6 | v2.7 |
|------|------|------|------|
| 001-nav-content-order | missed | caught | caught |
| 002-duplicate-affordance | missed | missed | caught |
| 003-dead-controls | missed | caught | caught |
| 004-label-parity | — | — | caught |
| 005-count-parity | — | — | caught |
| 006-reversible-nav | — | — | caught |

> Note on 001: the input is prose that names the divergence, so it tests that
> the v2.6 coupling step *fires* when given the structure — not the harder
> extract-from-a-screenshot path. A future image-based fixture would test that.

> Note on 002: found in the field — FLOWIE v2.6, run against its author's own
> NEAR AI concept prototype, evaluated three controls for one `legible ↔ raw`
> transition and passed each individually. The defect was the *multiplicity*.
> v2.7 adds the `single-affordance` invariant and the inverse-map `<affordance>`
> step that catches it.

> Note on 003: found in the field — FLOWIE v2.7, run against the
> agentic-trust-devtools "declarative trust surface." The surface's central
> object (the standing declaration) rendered three rule pills styled as controls,
> none wired; the only live control was one bottom link. Caught by the existing
> `control-has-effect` invariant (v2.6+) — no new check needed; logged to defend
> it against backslide, plus an **affordance-honesty corollary**: a styled
> control must be a control. Motivated making the declaration live (toggling
> `sponsored bias` re-ranks).

> Note on 004–006: **designed traps**, not field misses (issue #1) — one per
> invariant that had no coverage: `label-parity` (004), `count-parity` (005),
> `reversible-nav` (006). (`control-has-effect`, the fourth untrapped invariant
> when #1 was filed, got field case 003 first.) Unlike prose case 001, the
> inputs are HTML with the defect embedded but never named, so they exercise
> the extract-from-code path. v2.7 scores are from blind runs — the executing
> agent was given only the script and the input, not `expected.md`. Earlier
> columns are "—" (never run); fill them only from a real run, not a guess.

## Adding a case

Every real-world miss becomes the next case; designed traps are also welcome
when an invariant has no coverage (see 004–006). Number it sequentially, write
a tight `expected.md` that names the *specific* defect (not a vague heuristic)
plus the caught/partial/missed bar, and add a row to the scoring log.
