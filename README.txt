================================================================================
  OC-TOOLKIT + RBG_RUNNER
  Intelligent Agent Orchestrator for Open Code
================================================================================

WHAT IS OC-TOOLKIT?
--------------------
oc-toolkit is a ready-to-use library of agents, sub-agents, and skills for
Open Code (the OpenCode desktop app and CLI). Copy the folder structure into
your Open Code configuration directory and start using a full multi-agent
system immediately — no extra setup required.

The toolkit ships with 12 agents covering: idea planning, business strategy,
competitor research, social media, ads, email outreach, customer support,
finance, code generation, and deployment.


WHAT IS RBG_RUNNER?
--------------------
RBG_Runner is the intelligent orchestrator that sits above all other agents.
It:

  * Automatically discovers every agent in the toolkit
  * Reads workflow.json to understand schedules, dependencies, and conditions
  * Evaluates which agents are READY to run (schedule due, cooldown elapsed,
    dependencies met, conditions satisfied)
  * Triggers agents in the correct order, respecting hard rules:
      - code_generation always runs alone
      - deployment always runs last and alone
  * Logs every decision to .opencode/memory/runner_log.md
  * Tracks run history in .opencode/memory/run_history.json for cooldowns

RBG_Runner works two ways:
  1. As an OpenCode agent (rgb_runner.md) — invoked by the OpenCode app/CLI
  2. As a standalone Python script (rgb_runner.py) — run on a cron schedule
     from your OS scheduler (Task Scheduler on Windows, cron on Linux/Mac)


================================================================================
  FILE STRUCTURE
================================================================================

After installation, your Open Code config directory will look like this:

  %USERPROFILE%\.config\opencode\          (Windows)
  ~/.config/opencode/                       (Linux/Mac)
  │
  ├── opencode.jsonc                ← Main config — providers, instructions, paths
  │
  ├── agents/                       ← All agent definitions
  │   ├── rgb_runner.md             ← RBG_Runner OpenCode agent
  │   ├── rgb_runner.py             ← RBG_Runner Python orchestrator
  │   ├── workflow.json             ← Schedules, dependencies, conditions
  │   ├── RBG-Dev.md               ← Primary dev agent
  │   ├── 01_orchestrator.md       ← Task router
  │   ├── 02_idea_planner.md
  │   ├── 03_business_planning.md
  │   ├── 04_competitor_research.md
  │   ├── 05_social_media.md
  │   ├── 06_ads_management.md
  │   ├── 07_email_outreach.md
  │   ├── 08_code_generation.md
  │   ├── 09_customer_support.md
  │   ├── 10_finance.md
  │   └── 11_deployment.md
  │
  └── skills/                       ← Global instructions and skill definitions
      ├── 00_global.md              ← Identity, providers, RBG_* convention
      ├── 01_coding.md              ← Python/FastAPI coding standards
      ├── 02_workflow.md            ← Session start checklist, task lifecycle
      ├── 03_lessworks_active.md    ← Smallest-safe-diff philosophy
      ├── 04_skills_catalog.md      ← Skills index
      ├── fastapi_crud.md           ← FastAPI CRUD scaffold patterns
      ├── nvidia_api.md             ← NVIDIA API client patterns
      └── [35+ skill subdirectories]/
          └── SKILL.md              ← Individual skill definitions


Your projects also get a .opencode/ folder (gitignored):

  <your-project>/
  ├── RBG_README.md                 ← Read first every session
  ├── RBG_changelog.md             ← Append-only task history
  ├── RBG_todo.md                  ← Project backlog
  ├── RBG_tasks/                   ← Task JSON files
  └── .opencode/                   ← Agent-internal memory (gitignored)
      ├── memory/
      │   ├── context.md
      │   ├── run_history.json     ← RBG_Runner: last-run timestamps
      │   └── runner_log.md        ← RBG_Runner: decision log
      ├── rules/
      │   └── rules.md             ← Project-specific overrides
      └── skills/
          └── *.md                 ← Project-specific skills


================================================================================
  INSTALLATION
================================================================================

STEP 1 — Copy the agents/ and skills/ folders
----------------------------------------------
Copy the entire oc-toolkit folder structure into your Open Code config
directory. Do NOT rename the folders.

  Windows (Command Prompt):
    xcopy /E /I oc-toolkit\agents  "%USERPROFILE%\.config\opencode\agents"
    xcopy /E /I oc-toolkit\skills  "%USERPROFILE%\.config\opencode\skills"

  Linux/Mac (Terminal):
    cp -r oc-toolkit/agents  ~/.config/opencode/agents
    cp -r oc-toolkit/skills  ~/.config/opencode/skills

If the destination folders already exist, merge carefully — don't overwrite
any agent files you've already customised.


STEP 2 — Set your NVIDIA API key
---------------------------------
RBG_Runner uses NVIDIA's free LLM models. Set your API key as an environment
variable — NEVER put the key value directly in any config file.

  Windows (Command Prompt, permanent):
    setx NVIDIA_API_KEY "nvapi-YOUR-KEY-HERE"

  Windows (PowerShell, permanent):
    [Environment]::SetEnvironmentVariable("NVIDIA_API_KEY","nvapi-YOUR-KEY-HERE","User")

  Linux/Mac (add to ~/.bashrc or ~/.zshrc):
    export NVIDIA_API_KEY="nvapi-YOUR-KEY-HERE"

Get a free key at: https://integrate.api.nvidia.com


STEP 3 — Update opencode.jsonc
--------------------------------
Open your existing opencode.jsonc and merge in the configuration from
opencode_rbg_runner_snippet.jsonc.

Location:
  Windows: %USERPROFILE%\.config\opencode\opencode.jsonc
  Linux/Mac: ~/.config/opencode/opencode.jsonc

Sections to add/update:

  a) "providers" — add the nvidia-custom provider if not already present
  b) "instructions" — add the skills/ paths listed in the snippet
  c) "rgbRunner" — add the new RBG_Runner configuration block

IMPORTANT: Do not replace your entire opencode.jsonc. Only merge in what
you're missing. The snippet file contains comments explaining each section.


STEP 4 — Review workflow.json
------------------------------
workflow.json (agents/workflow.json) controls when each agent runs.
Open it and adjust the schedules and dependencies for your needs.

Default schedules:
  customer_support   — every 4 hours (highest priority)
  idea_planner       — Mondays at 09:00 UTC
  business_planning  — Mondays at 10:00 UTC (after idea_planner)
  competitor_research — Wednesdays at 09:00 UTC
  ads_management     — Tuesdays at 09:00 UTC
  email_outreach     — Tuesdays and Thursdays at 08:00 UTC
  finance            — 1st of each month at 09:00 UTC
  code_generation    — on-demand only
  deployment         — on-demand only, always last


STEP 5 — Restart Open Code
---------------------------
Close and reopen the Open Code app, or restart the OpenCode CLI.
The new agents and skills will be loaded automatically.


STEP 6 — Test the setup
------------------------
In Open Code, start a new session and ask:
  "Run RBG_Runner and show me which agents are ready to trigger."

Or test with the Python script:
  python agents/rgb_runner.py --list
  python agents/rgb_runner.py --dry-run


================================================================================
  SCHEDULED RUNS (Python Script)
================================================================================

rgb_runner.py can run on a system schedule so agents trigger automatically.

WINDOWS — Task Scheduler
  1. Open Task Scheduler → Create Basic Task
  2. Name: "RBG_Runner"
  3. Trigger: Daily / repeat every 30 minutes (or match your schedule)
  4. Action: Start a program
     Program: python
     Arguments: "%USERPROFILE%\.config\opencode\agents\rgb_runner.py" --trigger scheduled
  5. Finish

LINUX/MAC — Cron
  Run: crontab -e
  Add this line (runs every 30 minutes):
    */30 * * * * /usr/bin/python3 ~/.config/opencode/agents/rgb_runner.py --trigger scheduled

NOTE: The Python script respects the cron schedules in workflow.json — it
checks whether each agent's schedule is actually due before triggering it.
Running rgb_runner.py more frequently than your agents' schedules is safe:
agents will only trigger when their cron expression matches.


================================================================================
  HOW TO CUSTOMISE
================================================================================

ADD A NEW AGENT
---------------
1. Create a new .md file in agents/:
   agents/my_agent.md

   Use this frontmatter template:
   ---
   name: my_agent
   description: "Sub-agent · What this agent does"
   model: nvidia-custom/nvidia/nemotron-3.5-lightning-30b-a3b
   mode: subagent
   temperature: 0.2
   tools:
     bash: false
     write: true
     edit: true
     read: true
   ---

2. Add it to workflow.json under "agents":
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

3. Restart Open Code or re-run rgb_runner.py.
   RBG_Runner discovers new agents automatically on next run.


MODIFY A SCHEDULE
-----------------
Edit workflow.json and update the "schedule" field for the relevant agent.
Use standard 5-field cron syntax:
  MIN HOUR DAY MONTH WEEKDAY

  "0 9 * * 1"    → Every Monday at 09:00
  "0 */4 * * *"  → Every 4 hours
  "0 9 1 * *"    → First of each month at 09:00
  ""             → On-demand only (no schedule)

Cron tip: https://crontab.guru — visual cron expression builder


DEFINE AGENT DEPENDENCIES
--------------------------
In workflow.json, "depends_on" lists agents that must complete BEFORE
this agent can run in the same session:

  "social_media": {
    "depends_on": ["idea_planner"],
    ...
  }

This means social_media will not start until idea_planner has finished.
For scheduled runs, use "after:<agent>" conditions too:

  "conditions": ["after:idea_planner"]


SET A COOLDOWN
--------------
"cooldown_minutes" prevents an agent from running too frequently.
If an agent last ran 30 minutes ago and cooldown is 60, it will be skipped.

  "cooldown_minutes": 1440   → At most once per day
  "cooldown_minutes": 0      → No cooldown (always runs when conditions met)


ADD PROJECT-SPECIFIC RULES
---------------------------
Each project can override global rules and add its own skills:

  <your-project>/
  └── .opencode/
      ├── rules/
      │   └── rules.md      ← Rules that override global defaults for this project
      └── skills/
          └── my-skill.md   ← Skills specific to this project


================================================================================
  TROUBLESHOOTING
================================================================================

PROBLEM: "No agents ready to run"
  * Check workflow.json schedules — are they due? Use: python rgb_runner.py --list
  * Check cooldowns — has enough time elapsed since the last run?
  * Check conditions — are file_exists conditions pointing to real files?
  * Check dependencies — have depends_on agents completed this session?

PROBLEM: NVIDIA API errors (401 Unauthorized)
  * Verify NVIDIA_API_KEY is set: echo %NVIDIA_API_KEY% (Windows)
  * The key must start with "nvapi-"
  * Never put the key value in opencode.jsonc directly

PROBLEM: "workflow.json not found"
  * Run: python rgb_runner.py --init
  * This scaffolds a default workflow.json from your agents/ directory

PROBLEM: Agent runs but produces no output
  * Check .opencode/memory/runner_log.md for the last run's decision
  * Ensure the agent .md file exists in agents/
  * Confirm the agent's model is available (check your NVIDIA API plan)

PROBLEM: croniter not installed (scheduled triggers disabled)
  * Install it: pip install croniter python-dateutil pyyaml
  * Verify: python -c "import croniter; print('OK')"

PROBLEM: Skills not loading in Open Code
  * Confirm paths in opencode.jsonc use %USERPROFILE% (Windows) or $HOME (Linux/Mac)
  * Verify the skills/ folder was copied to the right config directory
  * Check for JSON syntax errors in opencode.jsonc (comments use // syntax)

PROBLEM: .opencode/ folder is showing in git status
  * Add .opencode/ to your project's .gitignore:
    echo ".opencode/" >> .gitignore
  * NEVER commit .opencode/ — it contains agent memory and run history


================================================================================
  SECURITY REMINDERS
================================================================================

  * NEVER hardcode your NVIDIA_API_KEY value in any file
  * NEVER log the key, even partially
  * NEVER commit .env files to git
  * NEVER commit .opencode/ to git
  * The key format is "nvapi-..." — if it appears in a diff, rotate it immediately
  * All paths in config files must use environment variables, not hardcoded usernames


================================================================================
  QUICK REFERENCE
================================================================================

Python script commands:
  python rgb_runner.py                          Evaluate and run ready agents
  python rgb_runner.py --dry-run                Show what would run (no execution)
  python rgb_runner.py --list                   List all agents and their status
  python rgb_runner.py --agent idea_planner     Force-run a specific agent
  python rgb_runner.py --init                   Scaffold workflow.json from agents/
  python rgb_runner.py --trigger scheduled      Mark run as scheduled (for logging)

Key files:
  agents/workflow.json                          Schedules, deps, conditions
  .opencode/memory/runner_log.md               Human-readable decision log
  .opencode/memory/run_history.json            Last-run timestamps (cooldowns)
  opencode_rbg_runner_snippet.jsonc            Config to merge into opencode.jsonc

Support:
  Open Code docs: https://opencode.ai/docs
  NVIDIA Free Models: https://integrate.api.nvidia.com

================================================================================
  END OF README
================================================================================
