# OC-Toolkit

**A ready-to-use library of agents, sub-agents, and skills for OpenCode.**

Copy the modular components directly into your OpenCode configuration and start using a full multi-agent system immediately — no extra setup required. Supports multiple LLM providers, with first-class support for NVIDIA's free model catalogue.

---

## What is OC-Toolkit?

OC-Toolkit gives you a complete, pre-wired agent ecosystem for OpenCode (both the desktop app and the CLI). The toolkit ships three things:

1. **Agents** — `.md` files that define agent behaviour, models, tools, and roles. OpenCode loads these as selectable agents in every session.
2. **RBG_Runner** — The intelligent orchestrator that sits above all other agents. It discovers agents automatically, reads a scheduling graph (`workflow.json`), evaluates readiness, and triggers agents in the correct dependency order.
3. **Skills** — Flat instruction files and structured skill directories that are injected into every session's system prompt, giving every agent access to consistent coding standards, platform patterns, and specialised knowledge.

---

## File Structure

```
oc-toolkit/
├── agents/                     ← All agent definitions + Python orchestrator
│   ├── rgb_runner.md           ← RBG_Runner — top-level orchestrator (OpenCode agent)
│   ├── rgb_runner.py           ← RBG_Runner — standalone Python orchestrator
│   ├── workflow.json           ← Scheduling graph: deps, crons, conditions, cooldowns
│   ├── RBG-Dev-seq.md          ← Primary dev agent — sequential
│   ├── RBG-Dev-Parallel.md     ← Primary dev agent — parallel task-sets
│   ├── rbg-fable-5.1.md        ← Primary dev agent — sequential, Fable 5.1
│   ├── tot_controller.md
│   ├── 01_orchestrator.md      ← Planner: worker + validator pairs (sequential or parallel)
│   ├── 02_idea_planner.md
│   ├── 03_business_planning.md
│   ├── 04_competitor_research.md
│   ├── 05_social_media.md
│   ├── 06_ads_management.md
│   ├── 07_email_outreach.md
│   ├── 08_code_generation.md
│   ├── 09_customer_support.md
│   ├── 10_finance.md
│   ├── 11_deployment.md
│   ├── 12_linkedin.md
│   ├── grounded_review.md      ← Default child validator (task / milestone / contract review)
│   ├── user_testing_validator.md ← Milestone behavior validator (runs the app)
│   └── tot_thinker.md
│
└── skills/
    ├── 00_global.md            ← Identity, providers, RBG_* memory convention
    ├── 01_coding.md            ← Python/FastAPI standards
    ├── 02_workflow.md          ← Session checklist, task lifecycle
    ├── 03_lessworks_active.md  ← Smallest-safe-diff philosophy
    ├── 04_skills_catalog.md    ← Skills index
    ├── fastapi_crud.md         ← FastAPI CRUD scaffold patterns
    ├── nvidia_api.md           ← NVIDIA API client patterns
    ├── SKILLS_README.md        ← Skills system overview
    │
    ├── ai-security/
    ├── api-design-reviewer/
    ├── api-test-suite-builder/
    ├── automation-engineer/
    ├── backend-api-engineer/
    ├── behuman/
    ├── devops-observability-engineer/
    ├── frontend-engineer/
    ├── fullstack-feature-builder/
    ├── lessworks/
    ├── playwright-pro/
    ├── prompt-governance/
    ├── python-engineer/
    ├── security-reviewer/
    ├── self-eval/
    ├── self-improving-agent/
    ├── senior-architect/
    ├── senior-backend/
    ├── senior-computer-vision/
    ├── senior-data-engineer/
    ├── senior-data-scientist/
    ├── senior-devops/
    ├── senior-frontend/
    ├── senior-fullstack/
    ├── senior-ml-engineer/
    ├── senior-prompt-engineer/
    ├── senior-qa/
    ├── senior-security/
    ├── skill-security-auditor/
    ├── skill-tester/
    ├── sql-database-assistant/
    ├── tech-stack-evaluator/
    ├── test-qa-engineer/
    └── threat-detection/
```

Each skill subdirectory contains a `SKILL.md` (the instruction file OpenCode loads) and a `SKILL_METADATA.json` (machine-readable metadata for discovery and tooling).

---

## Agents

### Primary Agents (mode: all)

These agents can be selected directly in the OpenCode UI or CLI. They have full tool access and act as entry points for user sessions.

| Agent | File | Description |
|---|---|---|
| **RBG_Runner** | `rgb_runner.md` | Top-level orchestrator. Discovers all agents, evaluates the workflow graph, and triggers ready agents in dependency order. Every triggered agent runs as a worker and must pass its validator (`grounded_review` / `contract_check`) before it counts as completed. Entry point for all automated and on-demand execution. Supports three execution modes: SINGLE RUN (default), BACKGROUND_HUMAN_REQUESTED, and BACKGROUND_PROPOSED (agent-initiated, requires explicit human approval). |
| **RBG-Dev-seq** | `RBG-Dev-seq.md` | Primary development agent — sequential. Plans through the Orchestrator and runs each task as worker → validator, one at a time. Full-stack coding, debugging, refactoring, and code review. Main agent for software development tasks. Reads `RBG_README.md` at session start, writes to `RBG_changelog.md`, respects `lessworks` (smallest-safe-diff) philosophy. |
| **RBG-Dev-Parallel** | `RBG-Dev-Parallel.md` | Parallel variant of RBG-Dev-seq (uses `BD_*` memory files). Designed for concurrent sub-task execution when multiple independent coding tasks can be dispatched simultaneously. |
| **RBG Fable 5.1** | `rbg-fable-5.1.md` | Sequential dev agent for Claude Fable 5.1 — same full workflow as RBG-Dev-Parallel (session resume, atomisation, ToT gate, grounded review, git checkpoints) but one task at a time. Uses `BD_*` memory files. |
| **ToT Controller** | `tot_controller.md` | Tree-of-Thought controller. Self-contained: simulates three thinker perspectives (conservative / balanced / creative) in two rounds within one call and synthesises a weighted verdict. Use for complex decisions requiring diverse reasoning. |

---

### Sub-Agents (mode: subagent)

These agents are invoked by orchestrators or by RBG_Runner. They are not selected directly in the OpenCode UI — they run as part of a larger workflow.

| Agent | File | Description |
|---|---|---|
| **Orchestrator** | `01_orchestrator.md` | Planner (sub-agent). Turns a goal into tasks where each task is a child **worker** (the domain agent) plus a child **validator** (`grounded_review` or `contract_check`) that must pass before the task counts as done. Returns a flat task list (`EXECUTION_MODE: sequential`) or grouped task-sets (`parallel`). |
| **Idea Planner** | `02_idea_planner.md` | Decomposes a high-level idea or goal into an ordered list of actionable tasks. Produces a structured task list that downstream agents can consume. |
| **Business Planning** | `03_business_planning.md` | Builds a business plan from a product or idea brief. Covers strategy, ideal customer profile (ICP), pricing model, KPIs, and go-to-market (GTM) approach. |
| **Competitor Research** | `04_competitor_research.md` | Researches the competitive landscape for a product or market. Produces structured competitor profiles: positioning, pricing, strengths, weaknesses, and differentiation opportunities. |
| **Social Media** | `05_social_media.md` | Drafts platform-native social copy for X/Twitter and LinkedIn. Takes a topic, angle, or brief and produces ready-to-post content tailored to each platform's norms. |
| **Ads Management** | `06_ads_management.md` | Plans and drafts Google Ads and Meta (Facebook/Instagram) campaigns. Covers audience targeting, ad copy, headline variants, and campaign structure recommendations. |
| **Email Outreach** | `07_email_outreach.md` | Writes cold email sequences and personalised outreach. Includes prospect research prompts, subject line variants, follow-up cadences, and reply templates. |
| **Code Generation** | `08_code_generation.md` | Generates production-ready code and tests from a specification. **Hard rule: always runs alone — never in parallel with any other agent.** Produces code with full test coverage and documentation. |
| **Customer Support** | `09_customer_support.md` | Classifies incoming customer support emails by topic and urgency, then drafts appropriate replies. Can be run on a schedule (default: every 4 hours) for inbox triage. |
| **Finance** | `10_finance.md` | Analyses business financial metrics: MRR, churn, LTV, CAC, burn rate, and spend breakdown. Takes raw data or summaries and produces structured financial reports. |
| **LinkedIn** | `12_linkedin.md` | All LinkedIn operations: posts, comments, replies, humanizing, hooks, content calendar, thread monitoring, engager analytics, profile optimisation, advocacy, repurposing, interviewing. Always draft → user approval → publish. |
| **Image Generation** | `13_image_generation.md` | Images from text with NVIDIA's hosted **FLUX.3 Image Klein**, falling back automatically to **FLUX.2 Klein 4B** if it is down, via `tools/nvidia_image_gen.py`. Writes the visual prompt, picks a valid size (multiples of 16, 512–1568 px), saves JPEGs to `assets/images/`, returns paths + seeds. Text-to-image only — the hosted API can't edit your own images. |
| **Deployment** | `11_deployment.md` | Handles deployment to Render and GitHub Actions. **Hard rule: always runs last in any session and always runs alone.** Manages environment config, deployment scripts, and rollback procedures. |
| **User Testing Validator** | `user_testing_validator.md` | Milestone behavior validator for missions (model `nvidia/nvidia/nemotron-3.5-super-vl-120b-a12b`). Starts the app, checks each behavior assertion in the milestone's validation contract against the running app (HTTP / CLI / Playwright), probes implied edge cases, scans logs, stops the app, and reports PASS / FAIL / BLOCKED per assertion with reproduction steps. Never edits code; local targets only. |
| **Grounded Review** | `grounded_review.md` | Default child validator. Audits any worker's output — claims, files actually written, and optional acceptance criteria (`GR_CRITERIA`) — and returns PROCEED / VERIFY_FLAGGED / BLOCK_AND_REDO. |
| **ToT Thinker** | `tot_thinker.md` | **Disabled (`disable: true`), unused.** Kept for reference — `tot_controller` is self-contained and never calls it. |

---

## Skills

Skills are instruction files that OpenCode injects into every agent's system prompt. They give all agents consistent knowledge without repeating it in each agent definition.

### Global Instruction Files (flat)

Loaded in order for every session. Earlier files take precedence.

| File | Purpose |
|---|---|
| `00_global.md` | Agent identity, NVIDIA provider configuration, RBG_* memory convention (README/changelog/todo/tasks pattern) |
| `01_coding.md` | Python/FastAPI coding standards, type hints, error handling, test conventions |
| `02_workflow.md` | Session start checklist, task lifecycle (pending → in-progress → done), commit discipline |
| `03_lessworks_active.md` | Smallest-safe-diff philosophy: never change more than necessary, prefer targeted edits over rewrites |
| `04_skills_catalog.md` | Index of all available skills and when to use each |
| `fastapi_crud.md` | FastAPI CRUD scaffold patterns: router setup, dependency injection, Pydantic schemas, response models |
| `nvidia_api.md` | NVIDIA API client patterns: async client setup, model selection, streaming, error handling |

### Skill Subdirectories

Each directory contains a `SKILL.md` with detailed instructions and a `SKILL_METADATA.json` for metadata. Many also include `examples.md`, `README.md`, and `validation.md`.

| Skill | Focus Area |
|---|---|
| `ai-security` | AI/ML system security: prompt injection defence, model output validation, adversarial input handling |
| `api-design-reviewer` | REST API design review: resource naming, HTTP semantics, versioning, pagination, error contracts |
| `api-test-suite-builder` | Automated API test generation: contract tests, integration tests, negative cases, load test scaffolds |
| `automation-engineer` | Workflow and process automation: scripting, scheduling, event-driven pipelines, CI hooks |
| `backend-api-engineer` | Backend API development: architecture patterns, database design, caching, authentication |
| `behuman` | Human-like communication: natural tone, empathy in AI output, avoiding robotic phrasing |
| `devops-observability-engineer` | DevOps and observability: logging, metrics, tracing, alerting, SLO/SLA definition |
| `frontend-engineer` | Frontend development: component architecture, state management, accessibility, performance |
| `fullstack-feature-builder` | End-to-end feature implementation: spec → backend → frontend → tests → deployment |
| `lessworks` | Deep implementation of the lessworks philosophy: minimal diffs, surgical edits, change justification |
| `playwright-pro` | Playwright browser automation: test authoring, page object model, CI integration, visual regression |
| `prompt-governance` | Prompt engineering governance: version control, eval frameworks, regression testing, documentation |
| `python-engineer` | Python best practices: packaging, typing, async patterns, performance profiling |
| `security-reviewer` | Security code review: OWASP Top 10, injection, auth flaws, secrets management, dependency auditing |
| `self-eval` | Self-evaluation patterns: agents assessing their own output quality before responding |
| `self-improving-agent` | Self-improvement loops: agents identifying their own weaknesses and iterating on solutions |
| `senior-architect` | Software architecture: system design, scalability decisions, trade-off analysis, ADRs |
| `senior-backend` | Senior backend engineering: distributed systems, event sourcing, service mesh, database internals |
| `senior-computer-vision` | Computer vision engineering: model selection, data pipelines, inference optimisation, evaluation |
| `senior-data-engineer` | Data engineering: pipeline design, data quality, orchestration (Airflow/Prefect), warehouse patterns |
| `senior-data-scientist` | Data science: experiment design, statistical rigour, model evaluation, bias detection |
| `senior-devops` | Senior DevOps: IaC, GitOps, multi-cloud, cost optimisation, incident response |
| `senior-frontend` | Senior frontend: micro-frontends, rendering strategies, Core Web Vitals, design systems |
| `senior-fullstack` | Senior fullstack: monolith-to-service decomposition, API gateway patterns, full-cycle ownership |
| `senior-ml-engineer` | ML engineering: training pipelines, model serving, MLOps, feature stores, drift detection |
| `senior-prompt-engineer` | Advanced prompt engineering: chain-of-thought, few-shot, structured outputs, evaluation |
| `senior-qa` | Senior QA: test strategy, risk-based testing, automation frameworks, quality gates |
| `senior-security` | Senior security engineering: threat modelling, zero-trust, cryptography, compliance (SOC2/GDPR) |
| `skill-security-auditor` | Skill/prompt security auditing: reviewing agent instructions for injection risks and over-privilege |
| `skill-tester` | Skill validation: testing that skill instructions produce correct and consistent agent behaviour |
| `sql-database-assistant` | SQL and database: query optimisation, index design, schema migration, query plan analysis |
| `tech-stack-evaluator` | Technology selection: evaluating frameworks, libraries, and platforms against project requirements |
| `test-qa-engineer` | Test engineering: unit/integration/e2e test authoring, mocking, coverage analysis |
| `threat-detection` | Threat detection engineering: SIEM rules, anomaly detection, log analysis, incident triage |

---

## Mission Mode — Long Goals That Check Themselves

For goals bigger than a handful of tasks, the dev agents and RBG_Runner run a **mission**:

| Role | Agent | What it does |
|---|---|---|
| Planner | `Orchestrator` (+ read-only child planners) | Asks only the questions that change the plan, writes a **validation contract** (numbered assertions defining "done") before any work, groups tasks into **milestones**, re-plans at every milestone |
| Workers | domain sub-agents | One task each with clean context; every output ends with a `=== HANDOFF ===` block (completed, not done, commands + exit codes, files, issues, assertions, procedure) |
| Task validator | `grounded_review` (GLM 5.3) | Checks each task against its assertions and handoff; the worker's own "done" is a claim, not evidence |
| Milestone validators | scrutiny: tests/types/lint + a fresh `grounded_review` per task · behavior: `user_testing_validator` (GLM 5.3 Flash) or `grounded_review` contract mode for non-code work | Does the milestone actually work end to end? |

Flow: **SCOPE → PLAN (contract + milestones) → approve → per task: planner → worker → validator → at each milestone: scrutiny + behavior validation → REPLAN** (continue / follow-up fixes / rescope with approval / escalate when the budget runs out) → repeat until every `must` assertion passes.

Progress is visible at a glance in `RBG_mission.md` / `BD_mission.md` at the project root (RBG_Runner keeps its missions in `.opencode/memory/missions/`). Writers run one at a time; only read-only work (planners, validators, research) runs in parallel. Validators use a different model family from most workers so they don't share blind spots.

---

## RBG_Runner — Orchestrator Deep Dive

RBG_Runner is the nerve centre of the toolkit. It operates in two forms:

**As an OpenCode agent** (`rgb_runner.md`) — invoked from the OpenCode UI or CLI. The agent reads, decides, and coordinates other agents through OpenCode's native agent-calling mechanism.

**As a standalone Python script** (`rgb_runner.py`) — run directly from the command line or on a system schedule (Windows Task Scheduler, Linux cron). Evaluates the workflow graph and triggers agents via the OpenCode CLI.

### Execution Modes

RBG_Runner determines its execution mode before triggering any agent:

**MODE 1 — SINGLE RUN** (default): Evaluates all agents, runs those that are READY, and exits. No loop, no approval needed.

**MODE 2 — BACKGROUND_HUMAN_REQUESTED**: Activated when the user explicitly requests a repeated schedule ("run 10 cycles every hour"). Presents a confirmation panel before starting. Never enters the loop without an explicit "yes" (or equivalent: "go", "approved", "start", "ok", "do it").

**MODE 3 — BACKGROUND_PROPOSED**: Activated after a completed single run when RBG_Runner determines that repeated execution would meaningfully advance the goal. Proposes the schedule to the user. Never proposes without completing at least one single run first. Falls back to SINGLE RUN if unattended (no terminal to receive approval).

### Python Script Commands

```bash
# Evaluate all agents and run those that are ready
python agents/rgb_runner.py

# Show what would run without executing anything
python agents/rgb_runner.py --dry-run

# List all agents and their current readiness status
python agents/rgb_runner.py --list

# Force-run a specific agent regardless of schedule/cooldown
python agents/rgb_runner.py --agent idea_planner

# Scaffold a default workflow.json from the agents/ directory
python agents/rgb_runner.py --init

# Mark this run as triggered by a scheduler (for logging)
python agents/rgb_runner.py --trigger scheduled

# Run 10 cycles every 60 minutes (asks for approval)
python agents/rgb_runner.py --cycles 10 --interval 60

# Run in background for up to 8 hours with a stated goal
python agents/rgb_runner.py --cycles 20 --interval 30 --duration 8 --goal "Generate and review 20 email drafts"

# Propose background execution after a single run
python agents/rgb_runner.py --propose-background
```

### workflow.json

The scheduling graph that controls when each agent runs. Lives at `agents/workflow.json`. Each entry defines:

```json
"agent_name": {
  "description": "What this agent does",
  "file": "agents/agent_name.md",
  "depends_on": ["other_agent"],
  "schedule": "0 9 * * 1",
  "timezone": "UTC",
  "conditions": ["file_exists:RBG_README.md"],
  "cooldown_minutes": 60,
  "priority": 10,
  "on_demand": false
}
```

Default schedules in the shipped `workflow.json`:

| Agent | Default Schedule |
|---|---|
| customer_support | Every 4 hours |
| idea_planner | Mondays 09:00 UTC |
| business_planning | Mondays 10:00 UTC (after idea_planner) |
| competitor_research | Wednesdays 09:00 UTC |
| ads_management | Tuesdays 09:00 UTC |
| email_outreach | Tuesdays + Thursdays 08:00 UTC |
| finance | 1st of month 09:00 UTC |
| code_generation | On-demand only |
| deployment | On-demand only, always last |

### Memory Convention

Agents write to these files in every project:

```
<your-project>/
├── RBG_README.md           ← Read at session start; summarises project state
├── RBG_changelog.md        ← Append-only log of completed work
├── RBG_todo.md             ← Backlog of pending tasks
├── RBG_tasks/              ← Individual task JSON files
└── .opencode/              ← Agent-internal memory (add to .gitignore)
    ├── memory/
    │   ├── context.md      ← Active constraints and current focus
    │   ├── run_history.json ← Last-run timestamps (used for cooldown checks)
    │   └── runner_log.md   ← RBG_Runner decision log
    └── rules/
        └── rules.md        ← Project-specific overrides
```

**Important:** Add `.opencode/` to your project's `.gitignore`. It contains agent memory and run history — never commit it.

---

## Installation

### Step 1 — Copy agents/ and skills/ into OpenCode config

```bash
# Windows (Command Prompt)
xcopy /E /I agents "%USERPROFILE%\.config\opencode\agents"
xcopy /E /I skills "%USERPROFILE%\.config\opencode\skills"

# Linux / macOS
cp -r agents ~/.config/opencode/agents
cp -r skills ~/.config/opencode/skills
```

### Step 2 — Set your NVIDIA API key

RBG_Runner uses NVIDIA's free LLM models. Set the key as an environment variable — **never put it in any config file.**

```bash
# Windows (permanent, Command Prompt)
setx NVIDIA_API_KEY "nvapi-YOUR-KEY-HERE"

# Linux / macOS (add to ~/.bashrc or ~/.zshrc)
export NVIDIA_API_KEY="nvapi-YOUR-KEY-HERE"
```

Get a free key at: https://integrate.api.nvidia.com

### Step 3 — Update opencode.jsonc

Merge the following into your existing `opencode.jsonc` (do not replace the whole file):

```jsonc
// Add to "instructions" array:
"C:/Users/<you>/.config/opencode/skills/00_global.md",
"C:/Users/<you>/.config/opencode/skills/01_coding.md",
"C:/Users/<you>/.config/opencode/skills/02_workflow.md",
"C:/Users/<you>/.config/opencode/skills/03_lessworks_active.md",
"C:/Users/<you>/.config/opencode/skills/04_skills_catalog.md",
"C:/Users/<you>/.config/opencode/skills/fastapi_crud.md",
"C:/Users/<you>/.config/opencode/skills/nvidia_api.md",
"C:/Users/<you>/.config/opencode/skills/**/*.md"

// Add "nvidia-custom" to the providers block (API key from env var only)
// Add the "rgbRunner" config block (see opencode.jsonc in this repo for reference)
```

### Step 4 — Review workflow.json

Open `agents/workflow.json` and adjust schedules and dependencies to match your workflow. Use https://crontab.guru to build cron expressions.

### Step 5 — Restart OpenCode

Close and reopen the OpenCode app or restart the CLI. New agents and skills load automatically.

### Step 6 — Test the setup

```bash
# In OpenCode: start a session with RBG_Runner and ask:
# "Run RBG_Runner and show me which agents are ready to trigger."

# Or from the command line:
python agents/rgb_runner.py --list
python agents/rgb_runner.py --dry-run
```

---

## Scheduled Runs (Python Script)

Run `rgb_runner.py` on a system schedule so agents trigger automatically without opening OpenCode.

**Windows — Task Scheduler:**
1. Open Task Scheduler → Create Basic Task
2. Trigger: Daily, repeat every 30 minutes
3. Action → Start a program:
   - Program: `python`
   - Arguments: `"%USERPROFILE%\.config\opencode\agents\rgb_runner.py" --trigger scheduled`

**Linux / macOS — cron:**
```bash
crontab -e
# Add:
*/30 * * * * /usr/bin/python3 ~/.config/opencode/agents/rgb_runner.py --trigger scheduled
```

Running `rgb_runner.py` more frequently than your agents' cron schedules is safe — agents only trigger when their schedule is actually due.

---

## Adding Your Own Agents

1. Create `agents/my_agent.md` with this frontmatter:

```yaml
---
name: my_agent
description: "Sub-agent · What this agent does"
model: nvidia/nvidia/nemotron-3.5-lightning-30b-a3b
mode: subagent
temperature: 0.2
tools:
  bash: false
  write: true
  edit: true
  read: true
---
```

2. Add it to `agents/workflow.json`:

```json
"my_agent": {
  "description": "What my agent does",
  "file": "agents/my_agent.md",
  "depends_on": [],
  "schedule": "0 9 * * 5",
  "timezone": "UTC",
  "conditions": [],
  "cooldown_minutes": 60,
  "priority": 50,
  "on_demand": true
}
```

3. Restart OpenCode. RBG_Runner discovers new agents automatically on the next run.

**Agent IDs = file names.** OpenCode registers each agent under its file name without `.md` (`agents/10_finance.md` → `10_finance`), not under the `name:` line. Use that ID when a primary agent calls it through the `task` tool (`subagent_type`) or from the CLI (`opencode run --agent 10_finance …`); `rgb_runner.py` maps workflow.json keys to IDs for you. If you add an agent, also add it to the *Agent IDs* table in each primary agent's "How to Call a Sub-agent" section.

---

## Security

- **NEVER** hardcode `NVIDIA_API_KEY` in any file
- **NEVER** log the key, even partially
- **NEVER** commit `.env` files to git
- **NEVER** commit `.opencode/` to git
- If the key value (`nvapi-...`) appears in a diff, rotate it immediately
- All config file paths must use environment variables, not hardcoded usernames

---

## Provider Configuration

The toolkit uses NVIDIA's free model catalogue. Agents use OpenCode's built-in `nvidia` provider (`model: nvidia/<NVIDIA model id>` — so most IDs start `nvidia/nvidia/…`; key from `NVIDIA_API_KEY`); the `nvidia-custom` provider in `opencode.jsonc` points at the same endpoint. Latencies from a live test on 2026-09-24:

| Model | Best For |
|---|---|
| `nvidia/nvidia/nemotron-3.5-super-vl-120b-a12b` | Orchestrator, RBG_Runner, idea/business/research agents, grounded_review, user_testing_validator, tot_controller, linkedin |
| `nvidia/nvidia/nemotron-3-ultra-550b-a55b` | code_generation (~5–13s) |
| `nvidia/nvidia/nemotron-3.5-lightning-30b-a3b` | deployment, ads_management, customer_support (~5s) |
| `nvidia/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` | finance (~4s) |
| `nvidia/meta/muse-glimmer-30b` | social_media, email_outreach (~8–16s) |
| `nvidia/z-ai/glm-5.3` | backup for planners and validators (~5–11s) |
| `nvidia/openai/gpt-oss-20b` | backup validator / coder (~8s) |

`nvidia/nvidia/nemotron-3-super-120b-a12b` was retired by NVIDIA on 2026-10-30 ("Model unavailable") and removed from every agent and backup list.

**Backup models:** OpenCode allows one model per agent, so each agent's ordered backup list lives in `agents/workflow.json` → `model_fallbacks`. `rgb_runner.py` and the agents retry with the next model when one is retired (410), missing (404), rate-limited (429) or times out. `heal_models.ps1` rewrites each agent's `model:` line to the first working model in its list — run it after a test shows a dead model, or weekly.

### Image generation (FLUX.3 Image Klein + automatic fallback)

`agents/13_image_generation.md` calls `tools/nvidia_image_gen.py` (standard-library Python, copy `tools/` to `~/.config/opencode/tools/`). It reads the key from `NVIDIA_API_KEY` or OpenCode's key store and never prints it.

```bash
python ~/.config/opencode/tools/nvidia_image_gen.py --prompt "a red fox in fresh snow at dawn" --width 1568 --height 672 --out fox.jpg
python ~/.config/opencode/tools/test_nvidia_image_gen.py     # full live test, report in tools/_image_test/
```

Verified live on 2026-10-30: endpoint `…/genai/black-forest-labs/flux-3-image-klein` (the `flux.3-…` form returns 404); width/height any multiple of 16 from 512 to 1568; steps 1–50; seed 0 = random, same seed = identical image; one JPEG per call in `artifacts[0].base64`; typical 3–15 s. Image editing with your own picture is **not** available on the hosted API (it only accepts NVIDIA's sample images).

**Fallback chain** (`python tools/nvidia_image_gen.py --list-models`): FLUX.3 Image Klein → FLUX.2 Klein 4B (same sizes, 1–4 steps, 3–5 s). Each model gets one same-model retry on 429/5xx/timeout, then the next model is tried on timeout, 404/410, 429, 5xx or an empty image; a 422 or a content-filter result stops immediately. Every request has a hard deadline (`--timeout`, default 120 s) because NVIDIA's gateway can hold a connection open without answering. Override the order with `--models a,b` or `NVIDIA_IMAGE_MODELS`, or pin one model with `--model`.

Probed on 2026-10-30 (`tools/probe_nvidia_image_models.py`): `flux.1-dev` and `flux.1-schnell` never answered (kept as opt-in only); `flux-3-image-klein-base`, `stable-diffusion-3.5-large`, `stable-diffusion-3-medium`, `stable-diffusion-xl`, `sdxl-turbo`, `qwen-image`, `qwen-image-2512` and `baidu/ernie-image` returned 404 for this account. Re-run the probe to re-check; `tools/test_image_fallback.py` re-tests the fallback.

### Keeping models healthy

NVIDIA retires models often (a 2026-09-24 test found ~half the catalog returning 410 "end of life"). Two scripts (in `tools/` here; copy them next to `opencode.jsonc` in `~/.config/opencode/`):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
& "$env:USERPROFILE\.config\opencode\test_models.ps1" -OnlyToolkit -Parallel 5   # which of the agents' models answer, and how fast
& "$env:USERPROFILE\.config\opencode\heal_models.ps1" -DryRun                    # what would change
& "$env:USERPROFILE\.config\opencode\heal_models.ps1"                            # point each agent at its first working model
python "$env:USERPROFILE\.config\opencode\agents\rgb_runner.py" --check-models  # same check from the Python runner
```

`heal_models.ps1` only rewrites the `model:` line, backs changed files up to `_model_heal_backup\<timestamp>\` (outside `agents\`, so OpenCode never loads the copies), and moves agents back to their primary model once it works again. Restart OpenCode after it changes anything.

All models are accessed through `https://integrate.api.nvidia.com/v1` using your `NVIDIA_API_KEY`.

---

## Troubleshooting

**"No agents ready to run"** — Check workflow.json schedules (`--list`), cooldowns (enough time since last run?), conditions (file_exists pointing to real files?), and dependencies (depends_on agents completed this session?).

**NVIDIA API 401 errors** — Verify `NVIDIA_API_KEY` is set in your environment (`echo %NVIDIA_API_KEY%` on Windows). Key must start with `nvapi-`.

**"workflow.json not found"** — Run `python rgb_runner.py --init` to scaffold a default from your agents/ directory.

**`Unknown agent: <name>` when a primary agent calls a sub-agent** — it sent the short name instead of the agent ID. IDs are file names (`10_finance`, `01_orchestrator`, …); see *Adding Your Own Agents*.

**`Model "…" is not available` / `Model unavailable` on a sub-agent call** — either the caller passed a model in the `task` call (it must not; each agent's own `model:` line is used) or the model was retired. Run `heal_models.ps1`, or update the agent's `model:` line and its list in `workflow.json → model_fallbacks`.

**croniter not installed** — Install with: `pip install croniter python-dateutil pyyaml`

**Skills not loading in OpenCode** — Confirm paths in `opencode.jsonc` are absolute and correct. Check for JSON syntax errors (the file supports `//` comments).

**`.opencode/` showing in git status** — Add `.opencode/` to your `.gitignore`: `echo ".opencode/" >> .gitignore`

---

## Links

- OpenCode documentation: https://opencode.ai/docs
- NVIDIA Free Models: https://integrate.api.nvidia.com
- Cron expression builder: https://crontab.guru
