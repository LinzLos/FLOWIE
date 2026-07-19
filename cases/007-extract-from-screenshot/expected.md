# Expected finding — Case 007

**The extraction-path fixture** (issue #2): the input is two real screenshots of
a loan-queue monitoring dashboard ("Queue Monitor — Refinance"), captured in
its Real Time and 1d-historical modes. Nothing names the defect; FLOWIE must
extract the structure — KPI cards, alert stack, capacity table, chart,
banners, time-range selector — read the numbers, and do the arithmetic.

## Input

- `input-realtime.png` — Real Time mode
- `input-1d.png` — 1d historical mode of the same screen

## Primary defect FLOWIE should surface

A **sign-convention contradiction** in the Net Flow metric, present in both
views:

> The NET FLOW card reads **−112**, while its own subtext reads **+203 in ·
> −91 out** — which nets to **+112** — and the chart banner for the same period
> reads **"+112 net today"**. (1d view: card **−89**, subtext +194 in · −105
> out → **+89**, banner **"+89 net yesterday"**.) One metric carries two
> opposite sign conventions on one screen. A user who reads −112 as "112 more
> out than in" concludes the backlog is *shrinking* — while the "Backlogging"
> badge and the banner mean the opposite. Pick one convention (backlog growth
> as positive matches the banner and badge) and use it on every surface.

## Secondary finding (strengthens a "caught")

> The header badge **"47 loans approaching risk"** is identical in both views
> while every other number changed (2,341→2,254 loans, 6.1→5.9 h, alerts
> reworded and re-counted). It is almost certainly live data not scoped by the
> time-range selector — so the historical view silently mixes one current-state
> number into a screen that claims to show yesterday.

## Deliberate non-defects (must NOT be flagged)

The 1d view removes the alert CTAs and the "Reassign Staff" button, adds the
"Actions unavailable in historical view" banner, and rewrites alerts in past
tense. That is *correct* mode coupling — controls that can't act on historical
data are removed and the mode is announced. Flagging these as missing controls
is an extraction/coupling error.

## Must include (to score "caught")

- Extracts the actual numbers and states the contradiction arithmetically
  (card sign vs its own in/out subtext vs the banner) in at least one view —
  not just "the numbers are confusing."
- States the user-facing consequence (opposite readings of whether the backlog
  is growing).
- Does not flag the 1d view's removed actions/past-tense copy as defects.

## Score "partial" if

- It notices tension between "−112" and "Backlogging"/banner without doing the
  in/out arithmetic that proves the contradiction, or flags it in vague
  "consider clarifying signage" terms — or catches only the secondary
  (47-loans) finding.

## Score "missed" if

- It critiques layout/heuristics without reading the numbers, or flags the
  deliberate historical-mode differences as the problem.

## Invariant this case defends

```
(extraction fidelity) + label-parity, generalized to values: every surface
showing the same metric must agree in value AND sign convention
```

Real artifact (not synthetic): captured 2026-07-18 from a working prototype.
Unlike prose case 001 and code cases 004–006, this is the image path — the
extract step has to read structure and numbers out of pixels before any
invariant can fire.
