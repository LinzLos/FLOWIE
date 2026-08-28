# Shift Prototype — Master Bug Inventory (2026-07-20, HEAD 387ea12)

The complete, deduplicated picture from five independent sweeps:
1. **FLOWIE v2.8** static invariant audit (14 findings — report `shift-prototype-2026-07-20-b.md`)
2. **React/runtime correctness review** (agent; every file traced; 8 findings, 4 novel)
3. **Data-layer computational sweep** (34 queues × 5 periods × ledger/simulation edges; 3 novel findings)
4. **Lint/type sweep** (eslint; 2 real findings)
5. **Live browser session** (full click-through: reproductions, dark mode, responsive, console)

Cross-references between sweeps are noted; each item appears once. IDs are stable for backlog use.

---

## A. Identity & ledger architecture — CRITICAL

**A1. Shared synthetic-name pool corrupts unrelated queues on any transfer** ⚠️ live-reproduced
`src/data/queues.ts:472` (FILL_NAMES), `QueueContext.tsx` (ledger keyed by bare name), consumers: `QueueMonitor.tsx:908`, `Performance.tsx:355`, `RosterModal.tsx:660`, `Roster.tsx:201`
All ~29 non-canonical queues draw from one 24-name pool: every one of the 24 names exists on 2+ queues (worst: Kenji Watanabe on **9**). The ledger keys by bare name, so one transfer edits every queue containing that name. Reproduced live: transferring Sana Qureshi into Debt-to-Income Assessment removed her from HMDA Compliance Audit (17 → 16 active) and would pin her as "NEW" on queues the user never touched. KPIs recompute over the corrupted rosters.
*Fix direction: unique per-queue synthetic identities (name variants per queue, or partitioned pools), or key the ledger by (name, homeQueue). This unblocks A2–A6.*

**A2. Loans drill-down ignores the ledger** — `queues.ts:742` (getLoans uses raw getWorkloads): departed specialists keep their loans on /loans; arrivals never receive any. [FLOWIE]

**A3. Post-departure count divergence** — move a canonical member out of Refinance: Roster reads "13 assigned · 9 more trained" but `getSourceQueues` (team.ts:195) yields 8 candidates. Parity only holds in the no-departure path. [FLOWIE]

**A4. Departures styled as arrivals** — `Roster.tsx:202` marks any `effectiveQueue !== assignedQueue` row `isNew`, so the SOURCE queue renders the departed specialist pinned on top with green fade + "Just assigned". Arrival semantics for a departure. [FLOWIE]

**A5. Transfers are irreversible** — once in the ledger a name is excluded from every future candidate pool (team.ts:196); no undo on the toast, no transfer-back path. [FLOWIE — partly a product decision: does the prototype need undo?]

**A6. Performance can divide by zero** — `Performance.tsx:364-368`: `handleAvg`/`teamTargetPct`/goal sub have no empty-roster guard; small 3-person queues can be drained via A1's global ledger → "NaNh / NaN%". [React review]

## B. Simulation — HIGH

**B1. Mid-run queue switch shows the run on the wrong queue** ⚠️ live-reproduced
`Simulation.tsx:1052-1071` (progress effect closes over the origin queue), `:477` (only the builder is pointer-disabled; the header QueueSelector stays enabled). Switch queues during the ~2.3s run: the new queue's screen shows "Running simulation" with the old queue's condition count; when the timer fires, results are written to the origin queue via the captured closure — the user never sees them complete. [FLOWIE + React review; verified: results DID land on the correct origin queue, so the write is right — the display is wrong]

**B2. Navigating away mid-run cancels the run** — unmount cleanup clears the `done` timer, so the scenario resumes as 'build'; contradicts the "a run in flight resumes as its result" contract comment (QueueContext.tsx:8). [FLOWIE + React review]

**B3. Share omits the queue** — `Simulation.tsx:1037-1043` encodes conditions only; hydration (`:995`) applies them to the recipient's current `selectedQueue` (default Refinance) and overwrites that queue's in-progress scenario without confirmation. A Clear-to-Close scenario link opens as a Refinance scenario. [FLOWIE + React review]

**B4. LTV rule stated with opposite comparators** — Queue Monitor rankings card: "LTV ≥ 80%" (under "Processing Status"); Simulation template: Current "≤ 80%" (under "Loan Risk Profile"); engine: ceiling with hardcoded ≥80 floor (simulation.ts:72). One rule, two directions, two factor names. [FLOWIE]

**B5. Ranking thresholds live in three unsynchronized copies** — RankingsCard strings (QueueMonitor.tsx:538-555), TEMPLATES (Simulation.tsx:47-68), CURRENT_THRESHOLDS (data/simulation.ts:48). Plus screen literals: target load "85" (QueueMonitor.tsx:750) duplicating `load−85` (queues.ts:675); `target='Refinance'` default (RosterModal.tsx:654). [FLOWIE]

**B6. setState-in-effect ×2** — `Simulation.tsx:208` (ConditionCard editVal sync) and `:330` (AddConditionForm proposed default): eslint react-hooks/set-state-in-effect; cascading-render pattern, works today. [lint]

## C. Charts & numbers — MEDIUM

**C1. Chart floor contradicts banners on 8 queue-period combos** — `queues.ts:600-601` `max(flow, 8)` floors both lines to 8=8 while the banner asserts "inflow has exceeded outflow": Non-Warrantable Condo Exception (all 5 periods) and USDA Loan Eligibility (Week/Month/Custom). [FLOWIE found 1 queue; data sweep found the full extent]

**C2. Performance right axis clips** — pinned 0–12h (Performance.tsx:189) but handle-time series starts at 1.13×avg: Manual Underwrite Exception (11.3h avg) draws ≈12.8h above the top tick. [FLOWIE]

**C3. Capacity-gap fudge** — `QueueMonitor.tsx:704` `max(0, gap − transferred×5)`: hardcoded 5/person, adjacent load cell unchanged, so gap ≠ load−85 after a transfer; `max(0,…)` masks genuine surplus on under-loaded queues. [FLOWIE]

**C4. Loan-ID prefix collision** — `queuePrefix` initials map both "Condo & Co-op Approval" and "Conditions Clearance" to "CC" with overlapping hash ranges: 30 duplicate loan IDs across the two queues. [data sweep]

## D. UX polish & a11y — LOW/MEDIUM

**D1. Escape collapses stacked layers at once** — QueueSelector popover + RosterModal both listen on document; `stopPropagation` can't suppress a sibling listener on the same node. Open dropdown → Tab away (popover only closes on outside *mousedown*/Escape/pick) → open modal → Escape closes BOTH; staged work lost. [React review]

**D2. Modal's source-queue dropdown has no own Escape** — pressing Escape to close the dropdown discards the entire modal and staged selections (RosterModal.tsx:414 pickerOpen). [React review]

**D3. Toast timer race** — `showToast`/`setToast` with bare `setTimeout(…, 4000)`, no clear: Save then Share within 4s → second toast dismissed early by the first's timer; timers also survive unmount (benign in React 19 but unclean). Same pattern ×3: Simulation.tsx:1027, QueueMonitor.tsx:947, Roster.tsx:391. [React review]

**D4. "1 specialists" pluralization** — RosterModal SummaryBar from/to lines ("1 specialists → 0 specialists"). Live-observed. [browser]

**D5. A11y gaps beyond the fixed trio** — CustomDatePicker popover: no Escape/containment; time-range `role="tab"` set: no arrow-key nav or tabpanel linkage; modal source picker: plain buttons, no listbox semantics; Loans/Roster/Performance tables: div grids without table/columnheader/aria-sort roles; Simulation legend hex `#5B9BD5` diverges from ChangePill tokens. (Contrast/focus-ring visibility remain unverified — needs a manual pass or tooling.) [FLOWIE]

**D6. Loans back pushes instead of popping** — browser-Back after using the back control returns to /loans in a loop (Loans.tsx:168). [FLOWIE, minor]

**D7. Responsive banner garble at ≤768px** — chart banner is a nowrap-stat flex row; when the text wraps, the stat interleaves mid-sentence ("for 4 **Backlog +112 today** straight days"); the narrow chart also leaves dead vertical space. Live-observed at 768px. [browser]

**D8. Dev-only lint noise** — react-refresh warnings on QueueContext.tsx (non-component exports); VizLab `any` ×2 (out of audit scope). No action needed beyond awareness. [lint]

---

## Verified clean (checked, no findings)

Route-state seeding (seed-once + clear; re-click same card works; no navigate loop) · dropdown pick sticks (live) · Simulation scenario persists across drill-down + origin-aware back (live) · one headcount per queue on the no-transfer path (34/34) · table↔modal candidate parity, empty ledger (34/34) · Refinance canon (14 / Σ91 / 6.1h / 8-of-14) · single canonical reassign control · outflow=inflow+net where displayed · simulation math edges (zero conditions → 0 affected; extreme/unparsable thresholds safe; no NaN) · insight strings under edge inputs · Overview-string ↔ getMetrics parsing parity (34/34) · source-queue integrity under single departures · loan urgent-count parity (34/34) · no console errors across a full interaction session · dark mode coherent on all screens · no horizontal overflow at 768px · CSS↔TSX class contract · list keys · type casts · ⌘K listener cleanup · StrictMode double-mount safety · render performance.

## Coverage limits

Static + scripted + one live click-through. Not covered: WCAG contrast ratios and focus-ring visibility (needs axe/manual), screen-reader behavior beyond markup, cross-browser (Chromium only), and long-session soak. Toast visibility after modal apply was inconclusive live (tool latency vs 4s TTL) — assumed working per code trace.

## Suggested severity ordering for backlog

1. A1 (unblocks A2–A4, A6) → 2. B1+B2 (one fix: freeze selector during run + persist 'running' outcome) → 3. B3 (share queue) → 4. C1+C3 (chart floor, gap fudge) → 5. B4+B5 (single source of ranking truth) → 6. C2, C4 → 7. D1–D4, D7 → 8. A5, D5, D6 (product-decision / polish tier).
