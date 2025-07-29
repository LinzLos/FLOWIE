🧩 FLOWIE v2.5
FLOWIE is a structured, LLM-native script designed to work cleanly with tools like ChatGPT, Claude, V0.dev, and Figma Make.

It acts as a pre-processing structure for AI builders, helping designers shape intent before generation. FLOWIE guides you through flow critique, design reasoning, and tradeoff evaluation—making your logic readable to both collaborators and machines.

Whether you're exploring AI-assisted design for the first time or leading systems-level UX strategy, FLOWIE supports faster, clearer outcomes by helping you:

- Reduce prompt churn and decision fatigue

- Generate multiple wireframe options quickly

- Evaluate usability tradeoffs with cognitive and perceptual heuristics

- Output structured schema for AI prototyping tools

✨ Flowie also introduces a lightweight agent model: assigning simple, role-based behaviors (like navigator, friction tester, and accessibility checker) to simulate UX perspectives and reduce the cognitive burden of solo ideation.

It’s also a powerful teaching and mentoring tool — great for guiding students, junior designers, and teams through the principles of human-centered UX critique and AI-augmented design workflows.

🚀 How to Use

You have three easy options:

1. Upload the `.txt` or `.xml` file into your LLM.
Then say:
``` 
Use this FLOWIE script to analyze a UI flow I'm about to describe.
```

2. Or with a slash command:
``` 
/slash_flowie_upload "Use this FLOWIE script to review the following UI steps..."
```

3. Copy and paste the FLOWIE content between `<instructions>` tags into your LLM.
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


🧪 Practitioner Feedback

These contributors actually used FLOWIE in their projects, offering grounded insight:
🙌 Contributors 

These contributors used FLOWIE in real projects and helped shape its development:
- **Taylor Cornelius** — Early tester of FLOWIE v1. Shared reactions and refinement opportunities after using it on live prototypes.    
- **Mubarak Haruna** — Used FLOWIE v2.2 on BRIDGEGOOD’s apprentice database; helped shape onboarding clarity and schema logic.

🧠 Design Feedback  
These contributors collaborated constructively on FLOWIE’s structure, usability, and direction:

- **Steve McMahon** — Gave detailed critique on file clarity, onboarding copy, selection metric logic, and inline usability comments.
- **Michael Paulus** — Recommended tool-specific schema selection and slash command initiation. Floated wizard-style model, which helped affirm FLOWIE's prompt-first focus.
- Shout out to Robert "Bobby" Renteria and Norm Sun on language onboarding clarification.
---

Created with ❤️ by Lindsay Zuñiga — 2025. Please credit when remixing or adapting. Feedback welcome.
