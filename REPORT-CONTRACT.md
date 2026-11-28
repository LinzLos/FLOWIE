# FLOWIE Report Contract

**Contract version:** 1.1
**Status:** the required output shape for every FLOWIE run — the subagent, the
sweep, and any manual run all emit to this.

## Why this exists

One structured output, three payoffs:

1. **Legible** — a reader learns the shape once and can scan any report fast.
2. **Composable** — two runs (or two versions, or FLOWIE alongside another
   checker) line up field-for-field in one roll-up.
3. **Publishable** — a stream of contract-shaped findings feeds the public
   catalog and a machine-readable ruleset with no rewriting.

Freeform prose is the thing this replaces. If a finding isn't in this shape,
it isn't a FLOWIE finding yet.

**Changed in 1.1 (2026-11-27, with script v2.10):** a finding's `kind` is
derived from its name instead of chosen (§4), `candidate:<name>` findings are
added, and the claim that deterministic findings never vary between runs is
replaced with what is true today. Reports that declare 1.0 are still read as
1.0.

---

## 1. The envelope (report header)

Every report opens with these fields:

| field | type | notes |
|---|---|---|
| `tool` | string | always `"FLOWIE"` |
| `script_version` | string | from `manifest.json` `current_version`, e.g. `"2.10"` |
| `contract_version` | string | the version of this contract, e.g. `"1.1"` |
| `target` | string | what was reviewed (path, URL, file list, or short description) |
| `target_type` | enum | `folder` \| `files` \| `url` \| `screenshot` \| `prose` \| `mcp` |
| `lens` | enum | `all` \| `navigator` \| `friction` \| `a11y` |
| `timestamp` | string | ISO 8601 |
| `invariant_failures` | integer | count of failing findings (severity ≥ low) |
| `counts` | object | `{critical, high, medium, low}` tallies |

---

## 2. The finding (the core unit)

Every finding carries the same fields, in this order:

| field | type | notes |
|---|---|---|
| `id` | string | stable within the report, e.g. `F1`, `F2` (reused for backlog references) |
| `invariant` | string | a named invariant from the script's library, e.g. `count-parity`; or `heuristic:<name>`; or `candidate:<name>`. No other names. See §4. |
| `kind` | enum | **`deterministic`** (a checkable fact) or **`judgment`** (an opinion, or a candidate). Derived from `invariant`, never chosen. See §4. |
| `severity` | enum | `critical` \| `high` \| `medium` \| `low` (see §3) |
| `location` | string | `file:line`, an element/selector, or a screen region |
| `defect` | string | what is wrong — specific, names the elements |
| `consequence` | string | → why a human cares (the user-facing result) |
| `source` | string | which lane caught it: `flowie` (default) \| `react` \| `data` \| `lint` \| `browser` — supports multi-sweep roll-ups |
| `verified` | boolean | `false` = coverage-limited / unverified; the report must say so |
| `fix` | string | optional — the fix direction |

The one-line human rendering of a finding:

```
[<invariant>] <location>: <defect> → <consequence>   (kind, severity, source[, unverified])
```

---

## 3. Severity scale

| severity | rank | means |
|---|---|---|
| `critical` | 4 | breaks a core task, corrupts data, or poisons every path through the flow |
| `high` | 3 | breaks a key interaction or view |
| `medium` | 2 | shows wrong/contradictory information, but contained |
| `low` | 1 | polish, minor a11y, cosmetic |

Findings are always listed **worst-first**.

---

## 4. The deterministic vs. judgment axis (required)

Every finding is marked `kind`, and the mark follows from the finding's name:

| the finding is named | its `kind` is |
|---|---|
| for an invariant in the script's `<invariants>` library | `deterministic` |
| `heuristic:<name>` | `judgment` |
| `candidate:<name>` | `judgment` |

- **`deterministic`** — a checkable fact: `count-parity: 6 ≠ 5`, `value-parity:
  −112 ≠ +112`. Anyone can re-check it by hand against the artifact. Only the
  named invariants earn this mark — as of script v2.10: `indexed-order`,
  `enumeration-order`, `label-parity`, `operand-order`, `value-parity`,
  `count-parity`, `control-has-effect`, `reversible-nav`, `single-affordance`.
- **`judgment`**, as `heuristic:<name>` — an expert opinion.
  `heuristic:cognitive-load — this screen asks a lot`. May vary run to run;
  that's expected, not a bug.
- **`judgment`**, as `candidate:<name>` — something that looks like a provable
  contradiction but matches no named invariant, e.g. `candidate:unit-mix — one
  card reads 6.1 h, the next 87 m`. It carries its evidence, and it stays
  judgment until the library gains an invariant (and a regression case) for it.

No other names are allowed. A run may not coin an invariant, stretch a named
one past its stated scope, or mark a heuristic or candidate `deterministic`.

What the mark does and does not promise. A deterministic finding is true or
false of the artifact, and checkable. It is not a promise that every run finds
it: while a model executes the checks, two runs of the same unchanged target
report overlapping but not identical sets. So a finding that is reported can be
verified, but a finding that is absent from a later run is not thereby fixed.

Why it's mandatory: a reader — or a build — must be able to tell a checkable
catch from an opinion at a glance, and a judgment finding that wobbles between
runs must read as *judgment*, not as a defect in FLOWIE. Mixing them unlabeled
destroys trust in both.

---

## 5. The body (three sections, always in this order)

1. **Findings** — worst-first, each in the finding shape above.
2. **Contract** — the change-impact checklist: the invariants that must hold for
   *this* flow, so a later edit to one side flags what else must change.
3. **Verified clean** — what was actively checked and passed. This *bounds* the
   findings: silence means "checked, fine," not "didn't look."

Then a closing **coverage** note: what was read, confidence level, and gaps
(what was not reachable, and why).

---

## 6. Machine form (source of truth)

The report is a JSON object. The human/HTML report is rendered from it.

```json
{
  "tool": "FLOWIE",
  "script_version": "2.10",
  "contract_version": "1.1",
  "target": "https://example.app/dashboard",
  "target_type": "url",
  "lens": "all",
  "timestamp": "2026-09-19T00:00:00Z",
  "invariant_failures": 2,
  "counts": { "critical": 1, "high": 0, "medium": 1, "low": 0 },
  "findings": [
    {
      "id": "F1",
      "invariant": "value-parity",
      "kind": "deterministic",
      "severity": "critical",
      "location": "Net Flow card / chart banner",
      "defect": "Net Flow card reads -112; the banner reads +112 for the same period",
      "consequence": "the same metric points two opposite directions — reader can't tell if the backlog is growing or draining",
      "source": "flowie",
      "verified": true,
      "fix": "pick one sign convention and use it on every surface"
    },
    {
      "id": "F2",
      "invariant": "heuristic:cognitive-load",
      "kind": "judgment",
      "severity": "medium",
      "location": "Alerts panel",
      "defect": "three simultaneous alerts compete for attention with no priority order",
      "consequence": "the user may act on the least important one first",
      "source": "flowie",
      "verified": true,
      "fix": ""
    }
  ],
  "contract": [
    "every surface showing a metric agrees in value AND sign convention",
    "nav.order === content.order"
  ],
  "verified_clean": [
    "label-parity across all tabs (5/5)",
    "reversible-nav on every drill-in"
  ],
  "coverage": "Loaded the rendered page; read all cards, alerts, and the chart. High confidence on structure and numbers. Not covered: the modal flows behind 'Reassign Staff' (not reached)."
}
```

---

## 7. Human form (rendered from the JSON)

```
FLOWIE REPORT · script v2.10 · contract v1.1
target: https://example.app/dashboard (url) · lens: all
INVARIANT FAILURES: 2   (critical 1 · high 0 · medium 1 · low 0)
—
F1 [value-parity] Net Flow card / chart banner  · CRITICAL · deterministic
    card reads -112, banner reads +112 for the same period
    → reader can't tell if the backlog is growing or draining
    fix: pick one sign convention, use it everywhere

F2 [heuristic:cognitive-load] Alerts panel  · MEDIUM · judgment
    three alerts compete with no priority order
    → user may act on the least important first
—
CONTRACT (must hold for this flow)
  • every surface showing a metric agrees in value AND sign
  • nav.order === content.order
—
VERIFIED CLEAN
  ✓ label-parity across all tabs (5/5)
  ✓ reversible-nav on every drill-in
—
COVERAGE: rendered page read in full; high confidence on structure + numbers.
Not covered: modal flows behind "Reassign Staff" (not reached).
```

---

## Conformance

A FLOWIE report is conformant if: it carries the full envelope, every finding
has all required fields (`id`, `invariant`, `kind`, `severity`, `location`,
`defect`, `consequence`, `source`, `verified`), findings are worst-first, and
all three body sections plus the coverage note are present. `kind` is never
omitted, and it matches the finding's name as §4 defines: `deterministic` only
for a named invariant, `judgment` for `heuristic:` and `candidate:` findings,
and no other names. When N = 0, state `INVARIANT FAILURES: 0` explicitly and still emit
the contract and verified-clean sections.
