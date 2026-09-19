# FLOWIE — working notes for Claude

FLOWIE is a versioned, LLM-native UX-flow critique script. `manifest.json`
points at the current version and at the report contract.

## Reports MUST follow the contract

Every FLOWIE report — from the `flowie` subagent, the sweep, or a manual run —
**must conform to [`REPORT-CONTRACT.md`](REPORT-CONTRACT.md)**. That file is the
single source of truth for the output shape (envelope, finding fields, the
required `deterministic` vs `judgment` mark, severity scale, and the three body
sections + coverage). Do not emit freeform report prose. If you are asked to
run FLOWIE or produce a FLOWIE report in this repo, read `REPORT-CONTRACT.md`
first and emit to it.

## Structure

- `scripts/versions/` — the versioned critique script; `manifest.json` points at current.
- `REPORT-CONTRACT.md` — the required report shape (machine JSON + human render).
- `cases/` — regression cases (named contradiction + input + expected + provenance); the scoreboard proves each version against the last.
- `.claude/agents/flowie.md` — the read-only `flowie` operator subagent.
- `operator/` — the sweep runner, sweep-targets, `SECURITY.md` (read-only + injection posture), and saved reports.

## Conventions

- Commit messages carry **no** AI-attribution trailer (no `Co-Authored-By`, no "Generated with").
- Versions are immutable snapshots; changes ship as a new version + CHANGELOG entry.
- Run `scripts/check_parity.sh` before cutting a release (the `.xml` and `.txt` must match).
