# Global Context — Brijesh Rathod's Environment

This file is loaded in every opencode session on this machine.

## Identity

You are working in **Brijesh Rathod's** development environment.
Primary agents: `RBG-Dev-seq` (sequential), `RBG-Dev-Parallel` (parallel task-sets), `rbg-fable-5.1` (sequential, Fable 5.1); `RBG_Runner` for scheduled/automated runs.

## Active Provider

Provider: OpenCode's built-in `nvidia` provider (reads NVIDIA_API_KEY). A full model ID is `nvidia/` + NVIDIA's own ID,
so most start with `nvidia/nvidia/…` — e.g. `model: nvidia/nvidia/nemotron-3.5-super-vl-120b-a12b`.
**When calling a sub-agent with the `task` tool, never pass a model** — each agent's own `model:` line is used.
**Agent IDs are file names** (`01_orchestrator`, `10_finance`, `12_linkedin`, `grounded_review` …), not the `name:` line —
use the ID for `subagent_type` and `opencode run --agent`.
`nvidia-custom` in opencode.jsonc points at the same endpoint and still works for manual use.
Models the agents use (all verified working):
- `nvidia/nvidia/nemotron-3.5-super-vl-120b-a12b` — planning, research, orchestration, validation, ToT
- ~~`nvidia/nvidia/nemotron-3-super-120b-a12b`~~ — RETIRED by NVIDIA ("Model unavailable", 2026-10-30) — do not use
- `nvidia/nvidia/nemotron-3-ultra-550b-a55b` — code generation, hardest reasoning (~5–13s)
- `nvidia/nvidia/nemotron-3.5-lightning-30b-a3b` — fast lightweight tasks: deployment, ads, support (~5s)
- `nvidia/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` — math, finance, step-by-step (~4s)
- `nvidia/meta/muse-glimmer-30b` — creative writing, social copy, email, LinkedIn (~8–16s)
- `nvidia/z-ai/glm-5.3` — validation (grounded_review, user_testing_validator, ToT) (~5–11s)
- `nvidia/openai/gpt-oss-20b` — backup validator / backup coder (~8s)
(Latencies from a live test on 2026-09-24. Backups per agent: agents/workflow.json → model_fallbacks.)

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
Primary Agents (mode: all — selectable entry points)
├── RBG_Runner        — scheduled / automated runs; every triggered agent is worker → validator
├── RBG-Dev-seq       — sequential full build cycle (RBG_* memory files)
├── RBG-Dev-Parallel  — parallel task-sets (BD_* memory files)
└── rbg-fable-5.1     — sequential full build cycle on Fable 5.1 (BD_* memory files)

Planner (mode: subagent)
└── 01_orchestrator   — goal → plan of child WORKER + child VALIDATOR pairs (sequential or parallel)

Workers (mode: subagent — do the domain work)
├── 02_idea_planner        — decomposes a plain-English idea into ordered tasks
├── 03_business_planning   — strategy, ICP, pricing, KPIs, go-to-market
├── 04_competitor_research — market and competitor analysis
├── 05_social_media        — X/Twitter and generic social copy
├── 06_ads_management      — Google Ads and Meta campaigns
├── 07_email_outreach      — cold email sequences
├── 08_code_generation     — production code + tests (reads stack.md + rules.md first)
├── 09_customer_support    — classify and reply to customer emails
├── 10_finance             — MRR, churn, LTV, spend analysis
├── 11_deployment          — Render / GitHub Actions deployment plans
├── 12_linkedin            — all LinkedIn operations (draft → approval → publish)
└── 13_image_generation    — images from text, NVIDIA FLUX.3 Image Klein → fallback FLUX.2 Klein 4B (tools/nvidia_image_gen.py)

Validators & decision support
├── grounded_review   — default child validator; audits any worker's output
├── user_testing_validator — milestone behavior validator; runs the app and checks the contract
├── tot_controller    — Tree-of-Thought verdict for hard decisions
└── tot_thinker       — disabled, unused (tot_controller is self-contained)
```

| Agent | File | Best For |
|---|---|---|
| RBG_Runner | rgb_runner.md | Scheduled / automated runs |
| RBG-Dev-seq | RBG-Dev-seq.md | PRIMARY — step-by-step build cycle |
| RBG-Dev-Parallel | RBG-Dev-Parallel.md | PRIMARY — faster runs with parallel task-sets |
| rbg-fable-5.1 | rbg-fable-5.1.md | PRIMARY — sequential build cycle on Fable 5.1 |
| Orchestrator | 01_orchestrator.md | Plan worker + validator pairs for multi-agent goals |
| Idea Planner | 02_idea_planner.md | Decompose goals into structured task lists |
| Business Planner | 03_business_planning.md | ICP, pricing, KPIs, go-to-market |
| Competitor Researcher | 04_competitor_research.md | Market analysis, gaps, SWOT |
| Social Media | 05_social_media.md | X/Twitter, generic social copy |
| Ads Manager | 06_ads_management.md | Google Ads, Meta campaigns |
| Email Outreach | 07_email_outreach.md | Cold email sequences |
| Code Generator | 08_code_generation.md | Production code + tests |
| Customer Support | 09_customer_support.md | Classify and reply to emails |
| Finance Analyst | 10_finance.md | MRR, churn, LTV |
| Deployment | 11_deployment.md | Render / GitHub Actions plans |
| LinkedIn | 12_linkedin.md | LinkedIn posts, comments, profile, analytics |
| Image Generation | 13_image_generation.md | Images from text (NVIDIA FLUX.3 Image Klein, fallback FLUX.2 Klein 4B) |
| Grounded Review | grounded_review.md | Validating any worker's output |
| User Testing Validator | user_testing_validator.md | Checking a milestone works end to end (missions) |
| ToT Controller | tot_controller.md | Hard decisions with real trade-offs |

## Missions (long goals)

Big goals run as missions: the Orchestrator scopes the goal, writes a validation contract
(numbered assertions = the definition of done) before any work, and splits the work into
milestones. Every task is planner → worker → validator; every worker ends with a
`=== HANDOFF ===` block; every milestone is checked by tests/reviews and by
`user_testing_validator` running the app; failures become follow-up tasks. Progress lives in
`RBG_mission.md` / `BD_mission.md` at the project root.

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
