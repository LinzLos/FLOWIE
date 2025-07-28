🧩 FLOWIE v2.5

FLOWIE is a structured, LLM-native script—designed to work cleanly with tools like ChatGPT, Claude, or builder platforms like V0.dev and Figma Make.

Whether you're exploring AI-assisted design for the first time or leading systems-level UX strategy, FLOWIE helps you:

- Reduce prompt churn and decision fatigue
- Generate multiple wireframe options quickly
- Evaluate usability tradeoffs with cognitive and perceptual heuristics
- Output structured schema for AI prototyping tools
FLOWIE is also a powerful teaching and mentoring tool—great for guiding students, junior designers, and teams through the principles of human-centered UX critique and AI-augmented design workflows.
---

🚀 How to Use

You have two easy options:

1. Upload the `.txt` or `.xml` file into your LLM
Then say:
``` 
Use this FLOWIE script to analyze a UI flow I'm about to describe.
```

Or with a slash command:
``` 
/slash_flowie_upload "Use this FLOWIE script to review the following UI steps..."
```

2. Copy and paste the FLOWIE content between `<instructions>` tags into your LLM
This is helpful if file upload isn’t available. The script will prompt you for missing info and guide you step-by-step.

---

🛠️ Features
- Built-in schema templates:
  - **Figma JSON Schema** — Structured output compatible with Figma Make’s auto-layout, component, and interaction definitions.
  - **Framer Schema** — Configured to align with Framer’s element hierarchy and animation primitives.
  - **V0-Compatible Skeleton** — Optional support for V0 (coming soon), geared toward low-code interface generation.
- Guided or Quick Start input options
- Support for complex flow variants (conditional, role-based, bulk)
- Built-in usability heuristic and display design evaluation
- JSON schema outputs tailored to tools like Figma, Framer (V0 coming soon)
- Designed to reduce hallucination through structured prompting

---

🙌 Contributors

🧪 Practitioner Feedback
These contributors actually used FLOWIE in their projects, offering grounded insight:

- **Taylor Cornelius** — Early tester of FLOWIE v1. Shared reactions and refinement opportunities after using it on live prototypes.
- **Susan Weisz** — Used FLOWIE and Figma Make to create a working prototype for a VDN Assignment Simulator.
- **Mubarak Haruna** — Applied FLOWIE to BRIDGEGOOD’s apprentice database; shaped improvements in accessibility, onboarding clarity, and schema integration.

🧠 Design Feedback
These contributors provided critique and strategic suggestions that helped shape FLOWIE's structure, clarity, and scope:

- **Steve McMahon** — Gave detailed critique on file clarity, onboarding copy, selection metric logic, and inline usability comments.
- **Michael Paulus** — Recommended tool-specific schema selection and slash command initiation. Floated wizard-style model, which helped affirm FLOWIE's prompt-first focus.
- **Vamsi Batchu** — Shared perspective on AI hallucination risks, balancing context, and LLM visual comprehension limits.
- **Robert “Bobby” Renteria** — Provided live feedback via Loom on language clarity, terminology comprehension, and user onboarding expectations. Suggested alternate interface ideas (e.g. form-based input), which helped clarify FLOWIE’s focus as a scriptable, adaptable prompt tool—not a hosted UI.
- **Norm Sun** — Offered microcopy and interaction design feedback that shaped early site experience, helping refine instructional hierarchy.

---

Created with ❤️ by Lindsay Zuñiga — 2025. Please credit when remixing or adapting. Feedback welcome.
