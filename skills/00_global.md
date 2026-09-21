# Global Context — Brijesh Rathod's Environment

This file is loaded in every opencode session on this machine.

## Identity

You are working in **Brijesh Rathod's** development environment.
Primary agent: `brijesh-dev` (orchestrator for all multi-step tasks).

## Active Provider

Provider: `nvidia-custom`
Available models (use these only — other providers are disabled):
- `nvidia/nemotron-3-ultra-550b-a55b` — complex reasoning, code generation
- `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` — math, finance, deterministic tasks
- `nvidia/nemotron-3.5-lightning-30b-a3b` — fast, lightweight tasks
- `meta/muse-glimmer-30b` — creative writing, social copy, email
- `google/gemma-4-31b-it` — ads, structured output, campaigns
- `z-ai/glm-5.3` — customer support, classification

## Project Memory Convention (RBG_* Pattern)

Every project uses this structure at its root:

```
<project_dir>/
├── RBG_README.md       ← READ THIS FIRST in any project session
├── RBG_changelog.md    ← append-only task history
├── RBG_todo.md         ← project backlog
├── RBG_tasks/          ← task JSON files (bdev-YYYYMMDD-NNN.json)
└── .opencode/         ← agent-internal memory (gitignored)
    ├── memory/
    ├── skills/
    └── rules/
```

**Always read `RBG_README.md` before starting any work in a project.**
If it does not exist, check with the user before assuming it's a new project.

## Agent Roster

```
Primary Agent
└── brijesh-dev            — orchestrates ALL multi-step work; the entry point

Sub-Agents (invoked internally by brijesh-dev, mode: subagent)
├── 01_orchestrator        — top-level planner; routes work to sub-agents
├── 02_idea_planner        — decomposes a plain-English idea into ordered tasks
├── 03_business_planning   — strategy, ICP, pricing, KPIs, go-to-market
├── 04_competitor_research — market and competitor analysis
├── 05_social_media        — X/Twitter and LinkedIn copy
├── 06_ads_management      — Google Ads and Meta campaigns
├── 07_email_outreach      — cold email sequences and prospect research
├── 08_code_generation     — production code + tests (reads stack.md + rules.md first)
├── 09_customer_support    — classify and reply to customer emails
├── 10_finance             — MRR, churn, LTV, spend analysis
└── 11_deployment          — Render / GitHub Actions deployment plans
```

| Agent | File | Best For |
|---|---|---|
| brijesh-dev | brijesh-dev.md | PRIMARY — orchestrates everything |
| Orchestrator | 01_orchestrator.md | Route complex tasks to the right sub-agents |
| Idea Planner | 02_idea_planner.md | Decompose goals into structured task lists |
| Business Planner | 03_business_planning.md | ICP, pricing, KPIs, go-to-market |
| Competitor Researcher | 04_competitor_research.md | Market analysis, gaps, SWOT |
| Social Media | 05_social_media.md | X/Twitter, LinkedIn copy |
| Ads Manager | 06_ads_management.md | Google Ads, Meta campaigns |
| Email Outreach | 07_email_outreach.md | Cold email sequences |
| Code Generator | 08_code_generation.md | Production code + tests |
| Customer Support | 09_customer_support.md | Classify and reply to emails |
| Finance Analyst | 10_finance.md | MRR, churn, LTV |
| Deployment | 11_deployment.md | Render / GitHub Actions plans |

## Instructions & Skills System

Global instructions are loaded in every opencode session via the `instructions` array in `opencode.jsonc`:

```jsonc
"instructions": [
  "C:/Users/kbrat/.config/opencode/skills/00_global.md",
  "C:/Users/kbrat/.config/opencode/skills/01_coding.md",
  "C:/Users/kbrat/.config/opencode/skills/02_workflow.md",
  "C:/Users/kbrat/.config/opencode/skills/03_lessworks_active.md",
  "C:/Users/kbrat/.config/opencode/skills/04_skills_catalog.md",
  "C:/Users/kbrat/.config/opencode/skills/**/*.md"
]
```

Each file path (or glob) is resolved and its content is appended to the system prompt for every session. Think of it as permanent background knowledge the model always has.

### File Inventory

| File | Purpose |
|---|---|
| `00_global.md` | Identity, provider, RBG_* convention, agent roster, this skills guide |
| `01_coding.md` | Python/FastAPI/SQLAlchemy standards, error handling, formatting |
| `02_workflow.md` | Session start checklist, task lifecycle, changelog protocol |
| `fastapi_crud.md` | Full CRUD scaffold: models, schemas, crud, router, tests |
| `nvidia_api.md` | NVIDIA API client patterns, model list, streaming, errors |

### Adding a New Global Skill

1. Create a new `.md` file under `skills/`:
   ```
   C:\Users\kbrat\.config\opencode\skills\<topic>.md
   ```

2. Use this template:
   ```markdown
   # Skill: <Topic Name>

   **When to use this skill:**
   <One or two sentences saying when this applies.>

   ---

   ## <Section>

   <Content — code templates, checklists, patterns>

   ---

   ## Checklist Before Delivering

   - [ ] Item 1
   - [ ] Item 2
   ```

3. No changes to `opencode.jsonc` needed — the glob `skills/**/*.md` already picks it up automatically.

### Project-Level Overrides

Each project can add its own rules and skills that take priority over these globals:

```
<project_dir>/
└── .opencode/
    ├── rules/
    │   └── rules.md      ← project-specific rules (override globals)
    └── skills/
        └── <topic>.md    ← project-specific skills (additive)
```

Project rules always win over global instructions.
