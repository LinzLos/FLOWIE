## Description
Reposition FLOWIE as **input/output tool-agnostic**. Input is framed by *modality* — a screenshot, code, a live URL, a written description — **and live MCP connections** from any source (e.g. a Figma MCP server, a browser/DOM MCP). Remove the V0/Figma/Framer builder-export templates and replace them with a neutral, agent-buildable implementation spec. Drop the hardcoded "back-of-house operations product" domain framing.

## Why
The value of FLOWIE is "screenshot or connect it to anything, and it critiques the flow" — not a fixed list of supported products. The current script privileges specific tools (Figma/Framer/V0 export, Figma-as-named-input, back-of-house domain), which has aged out of the actual workflow (agent + localhost + Netlify). Product names become one option among many; MCP is the agnostic live-input channel.

## Scope
Script edits across both `.xml` and `.txt` (keep them in sync — see #F4):
- `<artifacts>`: reframe by modality + add an **MCP connection** input type (any MCP source; Figma is just one example, not a hardcoded integration).
- `<schema_templates>` + `<ai_builder_schema>`: remove V0/Figma/Framer; emit a tool-agnostic build spec (structure / routes / components / state / interactions). Mention localhost + Netlify only as *examples*, not hardcoded targets.
- `<input>`: remove the "back-of-house operations product" framing.
- README: update "what it is" + Features/export claims to the agnostic + MCP framing.

## Recommended prerequisite
None (serializes with #F5 on the v2.7 script files).

## Touches
- scripts/versions/v2.7/* (shared — new version files, .xml + .txt)
- README.md

## Source
2026-06-14 review + direction: tool-stack shift (agent/localhost/Netlify), input-agnostic positioning, MCP as input channel.

## Owner
Lindsay.

## Acceptance criteria
- [ ] No V0/Framer product names; Figma demoted to one example MCP/artifact source, not a hardcoded integration
- [ ] MCP connection is a first-class input type, source-agnostic
- [ ] Export is a single neutral build spec; deploy targets (localhost/Netlify) are examples only
- [ ] `<input>` carries no domain-specific product framing
- [ ] README reframed to the agnostic + MCP identity
