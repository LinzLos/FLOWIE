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

> Note on 001: the input is prose that names the divergence, so it tests that
> the v2.6 coupling step *fires* when given the structure — not the harder
> extract-from-a-screenshot path. A future image-based fixture would test that.

> Note on 002: found in the field — FLOWIE v2.6, run against its author's own
> NEAR AI concept prototype, evaluated three controls for one `legible ↔ raw`
> transition and passed each individually. The defect was the *multiplicity*.
> v2.7 adds the `single-affordance` invariant and the inverse-map `<affordance>`
> step that catches it.

## Adding a case

Every real-world miss becomes the next case. Number it sequentially, write a
tight `expected.md` that names the *specific* defect (not a vague heuristic),
and add a row to the scoring log.
