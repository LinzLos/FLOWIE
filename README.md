# 🧩 FLOWIE v2.8

**FLOWIE is a design reviewer that never gets tired.** Show it whatever you have of an interface — a screenshot, code, a URL, a written description — and it finds the broken stuff: menus that don't match the page they index, buttons that look clickable but do nothing, screens you can't back out of, the same number telling two different stories on one screen. It caught every one of those in real prototypes; the receipts are in [`cases/`](cases/).

Under the hood, FLOWIE is a structured, versioned, machine-readable critique script that any LLM or agent can run. The point isn't a clever one-off prompt — the critique logic lives in a repo as an artifact: readable by both collaborators and machines, version-controlled, regression-tested, and reusable across projects. You improve the critique by editing the script and bumping the version — and every project that references FLOWIE picks up the change.

## What it is today

A single structured script (`.xml` + `.txt`, see `manifest.json` for the current version) that an LLM or agent can load and run. FLOWIE is **input/output tool-agnostic**: give it whatever you can capture — a screenshot, code, a live URL, a written description, or a **live MCP connection** from any source (a design-tool MCP server such as Figma's, a browser/DOM MCP, a project-specific server) — and it critiques the flow. Inputs are modalities, not a list of supported products. FLOWIE:

- **Extracts the structure** — reads the nav, content sections, controls, their order and labels — from whatever artifact you give it. You don't hand-inventory anything.
- **Checks coupling invariants** — verifies that coupled parts of the UI stay consistent: that a side nav's order matches the content it indexes, labels match their targets, counts line up, controls actually do something, and paths in have paths out.
- **Traces interactions** — evaluates what happens *after* an action (click a nav item → where do you land, in what order), not just how the screen looks at rest.
- **Applies usability heuristics** — Shneiderman's 8 Golden Rules and Wickens et al.'s 13 display-design principles.[^sources]
- **Outputs a contract** — a short checklist of the invariants that must hold, so a later edit to one side flags what else must change.
- **Exports a build spec** — a single tool-agnostic implementation spec (structure, routes, components, state, interactions) that any agent or builder can implement; deploy targets like localhost or Netlify are examples, not integrations.

It's also a clean teaching reference for human-centered UX critique — the structure makes the reasoning legible to students and junior designers, not just machines.

## The operator

FLOWIE is built to be operated, not just pasted — and the operator now exists
(issue #8):

- **On demand:** a `flowie` subagent ([`.claude/agents/flowie.md`](.claude/agents/flowie.md))
  loads whatever script `manifest.json` points at and runs it against any
  target — a prototype folder, files, screenshots, a live URL, or an MCP
  source, optionally scoped by lens. In a session in this repo: *"run flowie
  on ~/Dev/active/some-prototype"*. It contains no critique logic; the script
  stays the single source of truth.
- **Scheduled:** [`scripts/flowie-sweep.sh`](scripts/flowie-sweep.sh) runs the
  subagent over every target listed in
  [`operator/sweep-targets.txt`](operator/sweep-targets.txt), writes a dated
  report to `operator/reports/`, and exits nonzero when any invariant fails —
  wire it to cron/launchd (or a scheduled task) to get notified when a
  prototype breaks an invariant. Uncomment targets to enable them.

The operator is deliberately **read-only and injection-aware** — the critic's
tool allowlist can't execute or write, the sweep's orchestrator is equally
restricted, and instruction-like text found inside a target is reported as a
finding, never followed. The full threat model and the rules for running it
on client work are in [`operator/SECURITY.md`](operator/SECURITY.md).

Still ahead: registering the schedule itself, and richer notification routing.

## 🚀 How to use

The script lives in [`scripts/versions/`](scripts/versions/); `manifest.json` always points at the current version.

**30-second start (no setup, any LLM).** Download the current script file — [`flowie_v2.8.txt`](scripts/versions/v2.8/flowie_v2.8.txt) — upload it to Claude, ChatGPT, or any capable LLM together with whatever you have of your UI (a screenshot, code, a URL, or a written description), and say *"Use this FLOWIE script to review this flow."* That's the whole install.

**Claude Code users.** Clone the repo and open a session inside it — the [`flowie` subagent](.claude/agents/flowie.md) registers automatically, and *"run flowie on \<folder / files / URL\>"* runs the current release. [`scripts/flowie-sweep.sh`](scripts/flowie-sweep.sh) adds the scheduled sweep (see [The operator](#the-operator)); edit [`operator/sweep-targets.txt`](operator/sweep-targets.txt) to point at your own prototypes.

**Primary — reference it from an agent.** Point your agent at the current script file and have it run FLOWIE's passes against the project or artifact you're reviewing. Because it's versioned, the agent always reads the same defined logic, and updates propagate by bumping the version.

**Fallback — paste it into a chat.** If you don't have an agent set up, you can still upload the `.txt` or `.xml` to any LLM (ChatGPT, Claude) and say *"Use this FLOWIE script to analyze a UI flow I'm about to describe."* It will prompt you for anything it needs. This is the manual path — fine to start with, but the structure exists so you can automate past it.

## 🛠️ Features

- **Structure extraction** from screenshots, code, live URLs, prose, or a live MCP connection — no manual inventory, no privileged tool.
- **Coupling / invariant checks** against a named, extensible invariant library (indexed order, label parity, count parity, control-has-effect, reversible nav, single-affordance).
- **Interaction-consequence tracing** — reviews resulting state, not just resting layout.
- **Usability heuristics** — Shneiderman's 8 Golden Rules + Wickens et al.'s 13 display-design principles.
- **Tool-agnostic build-spec export** — structure / routes / components / state / interactions, implementable by any agent or AI builder.
- **Regression cases** in [`cases/`](cases/) — known failure modes FLOWIE should catch, so each version can be scored against the last.
- **Role-based critique lenses** — optional navigator / friction / a11y lenses that scope the existing passes to one perspective (wayfinding, effort, or assistive-tech use); with no lens selected, the full critique runs unchanged.
- **Guided or Quick Start** input; support for conditional, role-based, and bulk flow variants.

## 🙌 Contributors

People who used FLOWIE on real work and genuinely shaped it:

- **Taylor Cornelius** — Early tester of FLOWIE v1. Shared reactions and refinement opportunities after using it on live prototypes.
- **Mubarak Haruna** — Used FLOWIE v2.2 on BRIDGEGOOD's apprentice database; helped shape onboarding clarity and schema logic.

---

Created with ❤️ by Lindsay Zuñiga. Licensed [CC BY 4.0](LICENSE) — use, adapt, remix, and share freely; just credit the author. Feedback welcome.

[^sources]: Heuristic sources — **8 Golden Rules:** Shneiderman & Plaisant, *Designing the User Interface*. **13 Principles of Display Design:** Wickens, Lee, Liu & Gordon-Becker, *An Introduction to Human Factors Engineering* (2nd ed.). FLOWIE's framework, passes, and invariant logic are original; these established heuristic sets are credited to their authors.
