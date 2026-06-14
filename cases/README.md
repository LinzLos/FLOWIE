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

| Case | v2.5 | v2.6 |
|------|------|------|
| 001-nav-content-order | missed | — |

## Adding a case

Every real-world miss becomes the next case. Number it sequentially, write a
tight `expected.md` that names the *specific* defect (not a vague heuristic),
and add a row to the scoring log.
