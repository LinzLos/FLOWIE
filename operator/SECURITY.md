# Operator security posture

The sweep is an **unattended agent reading arbitrary prototype content** —
the combination that matters. The threat model has two heads: (1) content
inside a target steering the agent (prompt injection), and (2) an unattended
agent having the ability to execute or modify anything at all. The posture
is defense in depth: even if one layer fails, the next holds.

## Layers

1. **The critic is read-only by construction.** The `flowie` subagent's
   frontmatter allowlists `Read, Glob, Grep, WebFetch` only — no shell, no
   file writes, no edits. A critique needs eyes, not hands.
2. **The orchestrator is de-fanged too.** `flowie-sweep.sh` passes
   `--disallowedTools "Bash,Write,Edit,NotebookEdit"` to the headless run,
   so nothing above the subagent can execute or write either. The report file
   is produced by the shell's own output redirect, not by the model.
3. **Injection is treated as a finding, not a command.** The agent definition
   states that target content is data; instruction-like text found inside a
   prototype ("ignore your instructions", authority claims) is reported as a
   prompt-injection surface and never followed.
4. **Local and side-effect-free.** The sweep never modifies targets, never
   commits or pushes, and its only network traffic is the Claude API plus
   WebFetch of explicitly listed targets. A lock directory prevents
   overlapping runs; output lands only in `operator/reports/`.

## Residual risks (honest list)

- **Report poisoning.** Adversarial content can't make this agent *act*, but
  it could still confuse the critique into writing misleading report text.
  Reports are advisory; a human reads them before acting. Treat a report that
  urges you to run commands or visit links with the same suspicion as the
  content that produced it.
- **Machine account.** Headless runs use your local `claude` auth and run as
  your user. The layers above bound what a run can do, but protecting the
  account and machine itself (disk encryption, OS updates, screen lock) is
  outside this repo's control and still matters.
- **Secrets in prototypes.** The critique quotes what it reads and sends
  target content to the Claude API. Don't point the sweep at folders
  containing credentials or data you may not transmit.

## Rules for paid / client work

- **Written consent first.** Before running any agent over client code or
  designs, confirm the client permits third-party AI processing of their
  material. Target content goes to the model provider's API by necessity.
- **Read-only stays read-only.** Never loosen the tool allowlists for client
  targets; if a review needs a live browser or MCP session, do it supervised
  and interactively, not on the schedule.
- **Review `sweep-targets.txt` changes like code.** The targets file decides
  what the unattended agent reads; a bad entry is the easiest way to widen
  exposure.
- **Keep client reports out of the repo** if the repo is public or shared —
  `operator/reports/` is untracked by default; keep it that way for client
  material.
