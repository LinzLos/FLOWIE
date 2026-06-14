## Description
Fix the `.xml`↔`.txt` drift and prevent its recurrence. The v2.6 `.xml` is missing content the `.txt` has — the entire `<heuristics_reference>` block (Shneiderman 8 + Wickens 13) and a versionhistory entry — and `manifest.json` lists the `.xml` first, so the primary artifact is degraded.

## Why
The two files are hand-maintained and have already diverged, so a reader/agent gets a different (worse) FLOWIE depending on which file they load. Versions are immutable snapshots, so the fix lands in **v2.7**: its `.xml` and `.txt` must match, and a guard should stop them drifting again.

## Recommended prerequisite
Coordinate with #F3 and #F5 (all author the v2.7 script); this issue owns the *parity guarantee* at release.

## Scope
- Author v2.7 so `.xml` contains the `<heuristics_reference>` block + matching versionhistory (do **not** carry forward the v2.6 `.xml` omission). Note: the V0 export template is intentionally dropped by #F3, not restored.
- Add a parity guard: either generate one file from the other (single source of truth), or a simple diff check that the only `.xml`/`.txt` delta is the `.txt` usage-preamble wrapper.

## Touches
- scripts/versions/v2.7/* (shared)
- (optional) a small check script / note in CHANGELOG or cases on the parity rule

## Source
2026-06-14 review: `grep -c heuristics_reference` = 0 in `.xml`, present in `.txt`; structural diff confirms `<heuristics_reference>` + a versionhistory line are `.txt`-only.

## Owner
Lindsay.

## Acceptance criteria
- [ ] v2.7 `.xml` includes the heuristics_reference block + matching versionhistory
- [ ] v2.7 `.xml` and `.txt` differ only by the `.txt` usage preamble
- [ ] A documented guard exists so future drift is caught (generation or diff check)
