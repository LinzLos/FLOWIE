# FLOWIE Report Contract

**Contract version:** 1.0
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

---

## 1. The envelope (report header)

Every report opens with these fields:

| field | type | notes |
|---|---|---|
| `tool` | string | always `"FLOWIE"` |
| `script_version` | string | from `manifest.json` `current_version`, e.g. `"2.9"` |
| `contract_version` | string | the version of this contract, e.g. `"1.0"` |
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
| `invariant` | string | the named invariant, e.g. `count-parity`; or `heuristic:<name>` for a heuristic finding |
| `kind` | enum | **`deterministic`** (a fact — will reproduce) or **`judgment`** (an opinion — may vary). See §4. |
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

Every finding is marked `kind`:

- **`deterministic`** — a checkable fact. `count-parity: 6 ≠ 5`, `value-parity:
  −112 ≠ +112`. Same answer every run, zero variance. These are the invariants
  — FLOWIE's core.
- **`judgment`** — an expert opinion. `heuristic:cognitive-load — this screen
  asks a lot`. May vary run to run; that's expected, not a bug.

Why it's mandatory: a reader must be able to tell a rock-solid catch from an
opinion at a glance, and a judgment finding that wobbles between runs must read
as *judgment*, not as a defect in FLOWIE. Mixing them unlabeled destroys trust
in both.

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
  "script_version": "2.9",
  "contract_version": "1.0",
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
FLOWIE REPORT · script v2.9 · contract v1.0
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
omitted. When N = 0, state `INVARIANT FAILURES: 0` explicitly and still emit
the contract and verified-clean sections.
