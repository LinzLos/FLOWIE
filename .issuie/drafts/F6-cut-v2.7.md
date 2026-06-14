## Description
Cut the v2.7 release: create `scripts/versions/v2.7/`, bump `manifest.json` `current_version`, add a CHANGELOG entry, update the README version badge — shipping F3–F5.

## Why
F3–F5 all edit the script and ship as one version. This is the release/integration step.

## Recommended prerequisite
F3, F4, F5 (merged into the v2.7 script first).

## Scope
Versioning + release bookkeeping only.

## Touches
- manifest.json
- CHANGELOG.md
- README.md
- scripts/versions/v2.7/ (new dir; .xml + .txt)

## Source
Bundles the v2.6-review script findings into a release.

## Owner
Lindsay.

## Acceptance criteria
- [ ] manifest points at v2.7
- [ ] CHANGELOG has a v2.7 entry
- [ ] v2.6 dir preserved; .txt remains a real usage rendering (not the xml)
