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

| Case | v2.5 | v2.6 | v2.7 | v2.9 | v2.10 |
|------|------|------|------|------|-------|
| 001-nav-content-order | missed | caught | caught | caught | caught |
| 002-duplicate-affordance | missed | missed | caught | caught | caught |
| 003-dead-controls | missed | caught | caught | caught | caught |
| 004-label-parity | — | — | caught | caught | caught |
| 005-count-parity | — | — | caught | caught | caught |
| 006-reversible-nav | — | — | caught | caught | caught |
| 007-extract-from-screenshot | — | — | caught | partial | partial |
| 008-enumeration-order | — | — | — | caught | caught |

> v2.8 has no column: it was a licensing-only release with no behavioral change
> from v2.7, so v2.7's scores carry. A "—" means that version was never run on
> that case — fill a column from a real run, never a guess.

> v2.9 was scored on 2026-11-27 from blind runs: each run saw only the script,
> the report contract and the case input, under a neutral file name. For the
> prose cases (001 to 003) the title and the sentences that state the diagnosis
> were removed from the input first, so this column is a stricter test than the
> earlier ones.

> v2.10 was scored the same way on the same day, on the same cleaned inputs.
> All eight reports also passed `scripts/check_report.py` under contract 1.1:
> no heuristic or candidate marked deterministic, no named invariant marked
> judgment, and no invariant name outside the library.

> Note on 007 (v2.9 and v2.10): the sign contradiction was caught and proven
> arithmetically in both views, and the unchanged "47 loans" figure was noted.
> It scores partial because one judgment finding objected to the historical
> view removing the alerts' read-only links, which this case lists as a
> deliberate non-defect. v2.10 reports the contradiction under its own name,
> `value-parity`, and repeats the same objection.

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

> Note on 007: **the extraction-path fixture** (issue #2), resolving the caveat
> on case 001 — the input is two real screenshots (a loan-queue dashboard in
> Real Time and 1d modes), so the defect can only be found by reading structure
> and numbers out of pixels. Primary trap: a net-flow sign contradiction the
> run must prove arithmetically. Scored caught on a blind v2.7 run, which also
> surfaced unplanted real findings (a duplicate "Reassign Staff" control — the
> `single-affordance` invariant firing on a field artifact — and stale
> mode-coupling on badges and the specialist list).

> Note on 008: **field-motivated designed trap** — the ordering defect was
> found in the `shift-prototype` console (Overview cards rendered
> Outflow-left/Inflow-right while the product's own heading and Net Flow
> sub-label both named inflow first), then rebuilt as a code fixture so the
> divergence has to be extracted rather than read. Defends the **two invariants
> added in v2.9**, neither covered by the v2.8 set: `enumeration-order` (a label
> that names items in an order commits to that order — the prose sibling of
> `indexed-order`, which is scoped to nav-style controls) and `operand-order`
> (operands of a displayed derivation read in formula order; provable by
> arithmetic, as in 007). First scored from a blind run on 2026-11-27.

## Adding a case

Every real-world miss becomes the next case; designed traps are also welcome
when an invariant has no coverage (see 004–006). Number it sequentially, write
a tight `expected.md` that names the *specific* defect (not a vague heuristic)
plus the caught/partial/missed bar, and add a row to the scoring log.
