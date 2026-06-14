## Description
Add a regression case whose input is a real **screenshot or code artifact** (not prose), so the v2.6 structure-extraction step is tested end-to-end — extract the model, then catch the planted coupling defect.

## Why
v2.6's headline feature is "build the model from whatever artifact you're given." But case 001 feeds prose that already names the divergence, so extraction is never exercised. The repo's own README/001 note flags this as the missing harder fixture.

## Recommended prerequisite
None (independent of the script work; sequence after F1 only because both touch cases/README).

## Scope
One case folder with an image or code `input.*` and an `expected.md` that requires extracting structure before the defect is found.

## Touches
- cases/006-extract-from-artifact/
- cases/README.md (scoring log)

## Source
cases/README + case 001 caveat: "A future image-based fixture would test that."

## Owner
Lindsay.

## Acceptance criteria
- [ ] Input is a screenshot or code (not prose naming the divergence)
- [ ] expected.md requires correct extraction, then the coupling catch
- [ ] Scoring-log row added, marked as the extraction-path fixture
