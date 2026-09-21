#!/usr/bin/env python3
"""
RBG_Runner — Intelligent Agent Orchestrator for oc-toolkit
============================================================
Standalone Python runner for scheduled and on-demand agent coordination.
Discovers all agents, evaluates conditions and schedules, and triggers
the right agents in the right order.

Usage:
    python rgb_runner.py                    # evaluate and run ready agents
    python rgb_runner.py --agent idea_planner   # force-run a specific agent
    python rgb_runner.py --dry-run          # show what would run, do nothing
    python rgb_runner.py --list             # list all agents and their status
    python rgb_runner.py --init             # scaffold workflow.json from agents/

Requirements:
    pip install croniter pyyaml python-dateutil
"""

import argparse
import json
import logging
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Optional: croniter for cron-expression evaluation
try:
    from croniter import croniter
    CRONITER_AVAILABLE = True
except ImportError:
    CRONITER_AVAILABLE = False
    print("Warning: 'croniter' not installed — scheduled triggers disabled. "
          "Install with: pip install croniter", file=sys.stderr)

# Optional: pyyaml for frontmatter parsing
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    print("Warning: 'pyyaml' not installed — using regex fallback for frontmatter. "
          "Install with: pip install pyyaml", file=sys.stderr)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def resolve_config_dir() -> Path:
    """Return the opencode config directory using environment variables."""
    # Windows: %USERPROFILE%\.config\opencode
    # Linux/Mac: ~/.config/opencode
    if sys.platform == "win32":
        base = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    else:
        base = os.path.expanduser("~")
    return Path(base) / ".config" / "opencode"


CONFIG_DIR = resolve_config_dir()
AGENTS_DIR = CONFIG_DIR / "agents"
OPENCODE_INTERNAL = Path(".opencode")          # project-relative
RUN_HISTORY_FILE = OPENCODE_INTERNAL / "memory" / "run_history.json"
RUNNER_LOG_FILE = OPENCODE_INTERNAL / "memory" / "runner_log.md"
WORKFLOW_FILE = AGENTS_DIR / "workflow.json"

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("RBG_Runner")


# ---------------------------------------------------------------------------
# Agent Discovery
# ---------------------------------------------------------------------------

def parse_frontmatter(md_path: Path) -> dict:
    """Extract YAML frontmatter from a markdown agent file."""
    content = md_path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    raw = match.group(1)
    if YAML_AVAILABLE:
        try:
            return yaml.safe_load(raw) or {}
        except yaml.YAMLError:
            pass
    # Regex fallback — extracts simple key: value pairs
    result = {}
    for line in raw.splitlines():
        kv = re.match(r"^(\w+):\s*(.+)$", line)
        if kv:
            result[kv.group(1)] = kv.group(2).strip().strip('"')
    return result


def discover_agents(agents_dir: Path) -> dict[str, dict]:
    """
    Scan agents_dir for *.md files and return a registry.
    Keys are agent names (from frontmatter), values are metadata dicts.
    """
    registry: dict[str, dict] = {}
    if not agents_dir.exists():
        log.warning("Agents directory not found: %s", agents_dir)
        return registry

    for md_file in sorted(agents_dir.glob("*.md")):
        if md_file.name.startswith("_"):
            continue  # skip shared config files
        meta = parse_frontmatter(md_file)
        name = meta.get("name") or md_file.stem
        registry[name] = {
            "file": str(md_file),
            "name": name,
            "description": meta.get("description", ""),
            "model": meta.get("model", ""),
            "mode": meta.get("mode", "subagent"),
        }
    log.info("Discovered %d agent(s): %s", len(registry), ", ".join(registry))
    return registry


# ---------------------------------------------------------------------------
# Workflow Loading
# ---------------------------------------------------------------------------

def load_workflow(workflow_file: Path) -> dict:
    """Load workflow.json. Returns empty dict if file does not exist."""
    if not workflow_file.exists():
        log.warning("workflow.json not found at %s — run with --init to scaffold it.", workflow_file)
        return {}
    with open(workflow_file, encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            log.error("workflow.json is invalid JSON: %s", e)
            return {}


def scaffold_workflow(agents_registry: dict[str, dict], workflow_file: Path) -> None:
    """Create a default workflow.json from the discovered agents."""
    agents_section: dict[str, dict] = {}
    for name, meta in agents_registry.items():
        if name in ("RBG_Runner",):
            continue  # don't include the orchestrator itself
        agents_section[name] = {
            "description": meta.get("description", ""),
            "file": meta.get("file", ""),
            "depends_on": [],
            "schedule": "",
            "timezone": "UTC",
            "conditions": [],
            "cooldown_minutes": 60,
            "priority": 50,
            "on_demand": True,
        }
    workflow = {
        "_comment": "RBG_Runner workflow — define schedules, dependencies, and conditions for each agent.",
        "timezone": "UTC",
        "agents": agents_section,
    }
    workflow_file.parent.mkdir(parents=True, exist_ok=True)
    with open(workflow_file, "w", encoding="utf-8") as f:
        json.dump(workflow, f, indent=2)
    log.info("Scaffolded workflow.json → %s", workflow_file)
    print(f"\nworkflow.json created at: {workflow_file}")
    print("Review it and add schedules/dependencies as needed.\n")


# ---------------------------------------------------------------------------
# Run History
# ---------------------------------------------------------------------------

def load_run_history() -> dict:
    """Load last-run timestamps from .opencode/memory/run_history.json."""
    if RUN_HISTORY_FILE.exists():
        try:
            with open(RUN_HISTORY_FILE, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_run_history(history: dict) -> None:
    """Persist run history."""
    RUN_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RUN_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


# ---------------------------------------------------------------------------
# Condition Evaluation
# ---------------------------------------------------------------------------

def evaluate_conditions(conditions: list[str], completed_this_session: set[str]) -> tuple[bool, str]:
    """
    Evaluate a list of condition strings. Returns (passed, reason).

    Supported condition formats:
      file_exists:<path>        — True if file exists relative to cwd
      file_missing:<path>       — True if file does NOT exist
      after:<agent_name>        — True if agent already ran this session
    """
    for condition in conditions:
        if condition.startswith("file_exists:"):
            path = Path(condition.split(":", 1)[1])
            if not path.exists():
                return False, f"condition failed: file_exists:{path} (file not found)"
        elif condition.startswith("file_missing:"):
            path = Path(condition.split(":", 1)[1])
            if path.exists():
                return False, f"condition failed: file_missing:{path} (file exists)"
        elif condition.startswith("after:"):
            required_agent = condition.split(":", 1)[1]
            if required_agent not in completed_this_session:
                return False, f"condition failed: after:{required_agent} (not yet completed this session)"
        else:
            log.warning("Unknown condition format: %s (skipping)", condition)
    return True, "all conditions passed"


# ---------------------------------------------------------------------------
# Schedule Evaluation
# ---------------------------------------------------------------------------

def is_schedule_due(cron_expr: str, last_run_iso: Optional[str], timezone_str: str = "UTC") -> tuple[bool, str]:
    """
    Check if a cron schedule is due.
    Returns (due, reason).
    """
    if not cron_expr:
        return False, "no schedule defined (on-demand only)"
    if not CRONITER_AVAILABLE:
        return False, "croniter not installed — scheduled triggers disabled"

    now = datetime.now(timezone.utc)

    if last_run_iso:
        try:
            from dateutil.parser import parse as parse_dt
            last_run = parse_dt(last_run_iso)
        except Exception:
            last_run = None
    else:
        last_run = None

    try:
        cron = croniter(cron_expr, last_run or (now - __import__("datetime").timedelta(days=1)))
        next_run = cron.get_next(datetime)
        if next_run <= now:
            return True, f"cron match: {cron_expr} (next was {next_run.isoformat()})"
        return False, f"not yet due: next run {next_run.isoformat()}"
    except Exception as e:
        return False, f"cron parse error: {e}"


# ---------------------------------------------------------------------------
# Agent Readiness
# ---------------------------------------------------------------------------

def evaluate_agent(
    name: str,
    config: dict,
    run_history: dict,
    completed_this_session: set[str],
    now: datetime,
) -> tuple[bool, str]:
    """
    Determine if an agent is ready to run. Returns (ready, reason).
    """
    # 1. Cooldown check
    cooldown = int(config.get("cooldown_minutes", 60))
    last_run_iso = run_history.get(name)
    if last_run_iso:
        try:
            from dateutil.parser import parse as parse_dt
            last_run = parse_dt(last_run_iso)
            elapsed = (now - last_run).total_seconds() / 60
            if elapsed < cooldown:
                remaining = cooldown - elapsed
                return False, f"cooldown: {remaining:.0f} min remaining (cooldown={cooldown}m)"
        except Exception:
            pass

    # 2. Dependency check
    depends_on = config.get("depends_on", [])
    for dep in depends_on:
        if dep not in completed_this_session:
            return False, f"waiting for dependency: {dep}"

    # 3. Condition check
    conditions = config.get("conditions", [])
    if conditions:
        passed, reason = evaluate_conditions(conditions, completed_this_session)
        if not passed:
            return False, reason

    # 4. Schedule check (or on-demand)
    schedule = config.get("schedule", "")
    on_demand = config.get("on_demand", False)

    if schedule:
        tz = config.get("timezone", "UTC")
        due, reason = is_schedule_due(schedule, last_run_iso, tz)
        if not due:
            if on_demand:
                return False, f"schedule not due ({reason}) and on-demand only"
            return False, reason
        return True, f"scheduled: {reason}"

    if on_demand:
        return False, "on-demand only — not triggered by schedule"

    # No schedule and not on-demand: run on every invocation (after deps/conditions)
    return True, "always-run: no schedule restriction"


# ---------------------------------------------------------------------------
# Hard Execution Rules
# ---------------------------------------------------------------------------

NEVER_PARALLEL_WITH_ALL = {"code_generation"}
ALWAYS_LAST_ALONE = {"deployment"}


def apply_hard_rules(ready_agents: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """
    Enforce hard orchestration rules:
    - code_generation runs alone
    - deployment runs last and alone
    Returns an ordered list of (name, reason) tuples.
    """
    # Separate special agents
    code_gen = [(n, r) for n, r in ready_agents if n in NEVER_PARALLEL_WITH_ALL]
    deploy = [(n, r) for n, r in ready_agents if n in ALWAYS_LAST_ALONE]
    others = [(n, r) for n, r in ready_agents if n not in NEVER_PARALLEL_WITH_ALL and n not in ALWAYS_LAST_ALONE]

    # Build execution order: others → code_generation (alone) → deployment (alone, last)
    return others + code_gen + deploy


# ---------------------------------------------------------------------------
# Runner Log
# ---------------------------------------------------------------------------

def append_runner_log(
    trigger: str,
    evaluated: list[dict],
    selected: list[str],
    results: dict[str, str],
    next_scheduled: Optional[dict],
) -> None:
    """Append a human-readable entry to .opencode/memory/runner_log.md."""
    RUNNER_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    evaluated_lines = "\n".join(
        f"  - {e['name']}: {'✓ ready' if e['ready'] else '✗ skipped'} — {e['reason']}"
        for e in evaluated
    )
    result_lines = "\n".join(f"  - {k}: {v}" for k, v in results.items()) or "  (none)"
    next_info = (
        f"{next_scheduled['agent']} at {next_scheduled['at']}"
        if next_scheduled
        else "none scheduled"
    )

    entry = f"""
## [{ts}] RBG_Runner Run
- **Trigger**: {trigger}
- **Agents evaluated**:
{evaluated_lines}
- **Agents selected**: {', '.join(selected) or 'none'}
- **Results**:
{result_lines}
- **Next scheduled**: {next_info}
"""
    with open(RUNNER_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)


# ---------------------------------------------------------------------------
# Agent Execution
# ---------------------------------------------------------------------------

def run_agent(name: str, config: dict, dry_run: bool = False) -> str:
    """
    Trigger an agent. In a real OpenCode environment this would invoke
    the OpenCode CLI. Here we provide the hook and a dry-run simulation.

    Returns: "completed" | "failed" | "dry-run"
    """
    agent_file = config.get("file", "")
    if dry_run:
        log.info("[DRY-RUN] Would trigger: %s (%s)", name, agent_file)
        return "dry-run"

    log.info("Triggering agent: %s", name)

    # Hook: replace this with your actual OpenCode invocation.
    # Example using the OpenCode CLI (if available in PATH):
    #   result = subprocess.run(
    #       ["opencode", "run", "--agent", name],
    #       capture_output=True, text=True, timeout=300
    #   )
    #   return "completed" if result.returncode == 0 else "failed"

    # Fallback: log the intent and return completed
    log.info("Agent '%s' invoked (stub — wire up your OpenCode CLI call here)", name)
    return "completed"


# ---------------------------------------------------------------------------
# Main Orchestration Logic
# ---------------------------------------------------------------------------

def run_orchestration(
    force_agent: Optional[str] = None,
    dry_run: bool = False,
    trigger: str = "on-demand",
) -> dict:
    """
    Core orchestration loop. Returns a structured run report.
    """
    now = datetime.now(timezone.utc)
    session_id = now.strftime("%Y%m%d-%H%M%S")

    log.info("=== RBG_Runner session %s | trigger: %s ===", session_id, trigger)

    # Load registry and workflow
    agents_registry = discover_agents(AGENTS_DIR)
    workflow = load_workflow(WORKFLOW_FILE)
    workflow_agents = workflow.get("agents", {})
    run_history = load_run_history()

    completed_this_session: set[str] = set()
    evaluated: list[dict] = []
    results: dict[str, str] = {}

    # Force-run mode: bypass all checks for one specific agent
    if force_agent:
        config = workflow_agents.get(force_agent, {})
        config["file"] = config.get("file") or str(AGENTS_DIR / f"{force_agent}.md")
        result = run_agent(force_agent, config, dry_run)
        results[force_agent] = result
        if result == "completed":
            completed_this_session.add(force_agent)
            run_history[force_agent] = now.isoformat()
            save_run_history(run_history)
        append_runner_log(
            trigger=f"forced:{force_agent}",
            evaluated=[{"name": force_agent, "ready": True, "reason": "force-triggered"}],
            selected=[force_agent],
            results=results,
            next_scheduled=None,
        )
        return _build_report(session_id, trigger, agents_registry, evaluated, results, None)

    # Evaluate all workflow agents
    ready_agents: list[tuple[str, str]] = []
    for name, config in workflow_agents.items():
        # Skip the orchestrator itself
        if name in ("RBG_Runner", "rgb_runner"):
            continue
        ready, reason = evaluate_agent(name, config, run_history, completed_this_session, now)
        evaluated.append({"name": name, "ready": ready, "reason": reason})
        if ready:
            priority = int(config.get("priority", 50))
            ready_agents.append((name, reason, priority))  # type: ignore[arg-type]

    # Sort by priority (lower number = higher priority)
    ready_agents.sort(key=lambda x: x[2])  # type: ignore[index]
    ready_agents = [(n, r) for n, r, _ in ready_agents]  # type: ignore[misc]

    # Apply hard rules: code_generation alone, deployment last/alone
    ordered = apply_hard_rules(ready_agents)
    selected = [n for n, _ in ordered]

    if not selected:
        log.info("No agents ready to run this session.")
        append_runner_log(
            trigger=trigger,
            evaluated=evaluated,
            selected=[],
            results={},
            next_scheduled=_find_next_scheduled(workflow_agents, run_history, now),
        )
        return _build_report(session_id, trigger, agents_registry, evaluated, results, None)

    log.info("Execution order: %s", " → ".join(selected))

    # Execute agents in order
    for name, reason in ordered:
        config = workflow_agents.get(name, {})
        config.setdefault("file", str(AGENTS_DIR / f"{name}.md"))

        # Re-check dependencies now that prior agents have completed
        depends_on = config.get("depends_on", [])
        unmet = [d for d in depends_on if d not in completed_this_session]
        if unmet:
            log.warning("Skipping %s — unmet dependencies: %s", name, unmet)
            results[name] = f"skipped (unmet deps: {unmet})"
            continue

        result = run_agent(name, config, dry_run)
        results[name] = result

        if result in ("completed", "dry-run"):
            completed_this_session.add(name)
            if not dry_run:
                run_history[name] = now.isoformat()

    if not dry_run:
        save_run_history(run_history)

    next_sched = _find_next_scheduled(workflow_agents, run_history, now)
    append_runner_log(trigger, evaluated, selected, results, next_sched)
    return _build_report(session_id, trigger, agents_registry, evaluated, results, next_sched)


def _find_next_scheduled(workflow_agents: dict, run_history: dict, now: datetime) -> Optional[dict]:
    """Find the agent with the earliest upcoming scheduled run."""
    if not CRONITER_AVAILABLE:
        return None
    earliest = None
    earliest_name = None
    for name, config in workflow_agents.items():
        schedule = config.get("schedule", "")
        if not schedule:
            continue
        last_run = run_history.get(name)
        try:
            cron = croniter(schedule, last_run or now)
            nxt = cron.get_next(datetime)
            if earliest is None or nxt < earliest:
                earliest = nxt
                earliest_name = name
        except Exception:
            pass
    if earliest and earliest_name:
        return {"agent": earliest_name, "at": earliest.isoformat()}
    return None


def _build_report(
    session_id: str,
    trigger: str,
    agents_registry: dict,
    evaluated: list[dict],
    results: dict[str, str],
    next_scheduled: Optional[dict],
) -> dict:
    return {
        "runner_session": session_id,
        "trigger": trigger,
        "agents_discovered": len(agents_registry),
        "agents_evaluated": evaluated,
        "agents_selected": list(results.keys()),
        "results": results,
        "next_scheduled": next_scheduled,
    }


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="RBG_Runner — Intelligent Agent Orchestrator for oc-toolkit"
    )
    parser.add_argument(
        "--agent", metavar="NAME",
        help="Force-trigger a specific agent by name, bypassing schedule/cooldown checks",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show which agents would run without actually triggering them",
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List all discovered agents and their current readiness status",
    )
    parser.add_argument(
        "--init", action="store_true",
        help="Scaffold workflow.json from agents/ directory (safe — will not overwrite)",
    )
    parser.add_argument(
        "--trigger", default="on-demand",
        choices=["on-demand", "scheduled", "condition-met"],
        help="Declare what caused this run (for logging)",
    )
    args = parser.parse_args()

    if args.init:
        if WORKFLOW_FILE.exists():
            print(f"workflow.json already exists at {WORKFLOW_FILE} — delete it first to re-scaffold.")
            sys.exit(1)
        registry = discover_agents(AGENTS_DIR)
        scaffold_workflow(registry, WORKFLOW_FILE)
        sys.exit(0)

    if args.list:
        registry = discover_agents(AGENTS_DIR)
        workflow = load_workflow(WORKFLOW_FILE)
        run_history = load_run_history()
        now = datetime.now(timezone.utc)
        print(f"\n{'Agent':<30} {'Mode':<12} {'Schedule':<20} {'Last Run'}")
        print("-" * 80)
        for name, meta in sorted(registry.items()):
            config = workflow.get("agents", {}).get(name, {})
            schedule = config.get("schedule", "(on-demand)")
            last_run = run_history.get(name, "never")
            print(f"{name:<30} {meta.get('mode','?'):<12} {schedule:<20} {last_run}")
        print()
        sys.exit(0)

    report = run_orchestration(
        force_agent=args.agent,
        dry_run=args.dry_run,
        trigger=args.trigger,
    )

    print("\n" + "=" * 60)
    print("RBG_Runner Run Report")
    print("=" * 60)
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
