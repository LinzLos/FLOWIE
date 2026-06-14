# Changelog

All notable changes to FLOWIE are documented here. Versions track the script
in `scripts/versions/`; `manifest.json` always points at the current release.

## [2.7] — 2026-06

- Current release. Added the `single-affordance` invariant: a state transition
  should have one canonical control.
- New `<affordance>` step builds the inverse map (transition → controls) and
  flags any transition driven by more than one control (e.g., a segmented toggle
  duplicated by inline links), recommending which control is canonical.
- Motivated by a missed duplicate Legible/Raw toggle on an attestation card in
  the NEAR AI / IronClaw concept prototype; captured as regression case
  `cases/002-duplicate-affordance`.

## [2.6] — 2026-06

- Structure extraction: FLOWIE now builds its own model from
  whatever artifact it's given (screenshot, code, Figma, or prose) instead of
  asking the user to inventory the UI.
- Cross-component coupling checks against a named invariant library (indexed
  order, label parity, count parity, control-has-effect, reversible nav).
- Interaction-consequence tracing — evaluates the state after an action, not
  just the resting layout.
- Graceful coverage handling: asks for more input only when a check is blocked,
  otherwise marks findings unverified and proceeds.
- Invariants/contract output as a change-impact checklist.
- Motivated by a missed nav↔content order mismatch; captured as regression
  case `cases/001-nav-content-order`.

## [2.5] — 2025-07

- Built-in schema templates (Figma JSON, Framer, V0-compatible skeleton).
- Guided or Quick Start input options; support for conditional, role-based, and bulk flow variants.
- Built-in usability heuristic and display-design evaluation.
- Lightweight agent model (navigator, friction tester, accessibility checker).

## [2.2]

- Used in real projects (e.g. BRIDGEGOOD apprentice database); refined onboarding clarity and schema logic.

## [1.x]

- Initial public versions and early practitioner testing.
