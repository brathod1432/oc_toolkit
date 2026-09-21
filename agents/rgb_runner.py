#!/usr/bin/env python3
"""
RBG_Runner — Intelligent Agent Orchestrator for oc-toolkit
============================================================
Three execution modes:

  SINGLE (default)
    Runs all READY agents once and exits. No approval needed.

  BACKGROUND_HUMAN_REQUESTED
    Human explicitly asks for repeated runs (--cycles / --interval / --duration).
    Agent confirms the schedule, waits for approval, then loops.

  BACKGROUND_PROPOSED  (--propose-background)
    Agent completes one SINGLE run, then evaluates whether looping would help.
    If yes, proposes a schedule to the human and waits for approval.

  BYPASS MODE  (--bypass)
    Skips ALL human approval gates. The agent decides autonomously on cycles,
    interval, and mode, then proceeds without waiting for confirmation.
    Session-scoped — does not persist between sessions.
    Still logs everything to runner_log.md as normal.

Background loops NEVER start without an explicit human "yes" in the current
session (unless bypass mode is active). If running unattended (--unattended),
always falls back to SINGLE.

Usage examples:
  python rgb_runner.py                                          # SINGLE RUN
  python rgb_runner.py --cycles 10 --interval 60               # BACKGROUND (human-requested, asks to confirm)
  python rgb_runner.py --cycles 5 --interval 60 --duration 5   # BACKGROUND with explicit duration cap
  python rgb_runner.py --propose-background                     # run once, then propose if useful
  python rgb_runner.py --bypass                                 # skip all approval gates (autonomous)
  python rgb_runner.py --bypass --cycles 5 --interval 30       # bypass + explicit schedule
  python rgb_runner.py --agent idea_planner                     # force-run one agent (single)
  python rgb_runner.py --dry-run                                # show what would run, no execution
  python rgb_runner.py --list                                   # list agents + readiness
  python rgb_runner.py --init                                   # scaffold workflow.json
  python rgb_runner.py --unattended --trigger scheduled         # safe for cron (always SINGLE)

Requirements:
  pip install croniter pyyaml python-dateutil
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

# ── Optional dependencies ──────────────────────────────────────────────────

try:
    from croniter import croniter
    CRONITER_AVAILABLE = True
except ImportError:
    CRONITER_AVAILABLE = False
    print("Warning: 'croniter' not installed — scheduled triggers disabled. "
          "pip install croniter", file=sys.stderr)

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# ── Configuration ──────────────────────────────────────────────────────────

def resolve_config_dir() -> Path:
    """Return the opencode config directory using environment variables only."""
    if sys.platform == "win32":
        base = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    else:
        base = os.path.expanduser("~")
    return Path(base) / ".config" / "opencode"


CONFIG_DIR = resolve_config_dir()
AGENTS_DIR = CONFIG_DIR / "agents"
OPENCODE_INTERNAL = Path(".opencode")
RUN_HISTORY_FILE  = OPENCODE_INTERNAL / "memory" / "run_history.json"
RUNNER_LOG_FILE   = OPENCODE_INTERNAL / "memory" / "runner_log.md"
WORKFLOW_FILE     = AGENTS_DIR / "workflow.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("RBG_Runner")

# ── Data Structures ────────────────────────────────────────────────────────

@dataclass
class BackgroundSession:
    """Carries all parameters for a background execution loop."""
    cycles_total: int
    interval_minutes: int
    duration_hours: Optional[float]       # None = no wall-clock cap
    goal: str = ""
    approved: bool = False
    cycles_completed: int = 0
    started_at: Optional[datetime] = None
    mode: str = "BACKGROUND_HUMAN_REQUESTED"   # or BACKGROUND_PROPOSED
    bypass: bool = False                        # True = approval was skipped

    @property
    def estimated_end(self) -> Optional[datetime]:
        if self.started_at is None:
            return None
        by_cycles = self.started_at + timedelta(
            minutes=self.interval_minutes * self.cycles_total
        )
        if self.duration_hours is not None:
            by_duration = self.started_at + timedelta(hours=self.duration_hours)
            return min(by_cycles, by_duration)
        return by_cycles

    @property
    def stop_condition_reached(self) -> bool:
        if self.cycles_completed >= self.cycles_total:
            return True
        if self.duration_hours is not None and self.started_at is not None:
            elapsed = (datetime.now(timezone.utc) - self.started_at).total_seconds() / 3600
            if elapsed >= self.duration_hours:
                return True
        return False


# ── Agent Discovery ────────────────────────────────────────────────────────

def parse_frontmatter(md_path: Path) -> dict:
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
    result = {}
    for line in raw.splitlines():
        kv = re.match(r"^(\w+):\s*(.+)$", line)
        if kv:
            result[kv.group(1)] = kv.group(2).strip().strip('"')
    return result


def discover_agents(agents_dir: Path) -> dict[str, dict]:
    registry: dict[str, dict] = {}
    if not agents_dir.exists():
        log.warning("Agents directory not found: %s", agents_dir)
        return registry
    for md_file in sorted(agents_dir.glob("*.md")):
        if md_file.name.startswith("_"):
            continue
        meta = parse_frontmatter(md_file)
        name = meta.get("name") or md_file.stem
        registry[name] = {
            "file": str(md_file),
            "name": name,
            "description": meta.get("description", ""),
            "model": meta.get("model", ""),
            "mode": meta.get("mode", "subagent"),
        }
    log.info("Discovered %d agent(s)", len(registry))
    return registry


# ── Workflow ───────────────────────────────────────────────────────────────

def load_workflow(workflow_file: Path) -> dict:
    if not workflow_file.exists():
        log.warning("workflow.json not found — run with --init to scaffold it.")
        return {}
    with open(workflow_file, encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            log.error("workflow.json invalid JSON: %s", e)
            return {}


def scaffold_workflow(agents_registry: dict[str, dict], workflow_file: Path) -> None:
    agents_section: dict[str, dict] = {}
    for name, meta in agents_registry.items():
        if name in ("RBG_Runner",):
            continue
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
        "_comment": "RBG_Runner workflow — define schedules, dependencies, and conditions.",
        "timezone": "UTC",
        "agents": agents_section,
    }
    workflow_file.parent.mkdir(parents=True, exist_ok=True)
    with open(workflow_file, "w", encoding="utf-8") as f:
        json.dump(workflow, f, indent=2)
    log.info("Scaffolded workflow.json → %s", workflow_file)
    print(f"\nworkflow.json created at: {workflow_file}")
    print("Review it and add schedules/dependencies as needed.\n")


# ── Run History ────────────────────────────────────────────────────────────

def load_run_history() -> dict:
    if RUN_HISTORY_FILE.exists():
        try:
            with open(RUN_HISTORY_FILE, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_run_history(history: dict) -> None:
    RUN_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RUN_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


# ── Condition / Schedule Evaluation ───────────────────────────────────────

def evaluate_conditions(conditions: list[str], completed_this_session: set[str]) -> tuple[bool, str]:
    for condition in conditions:
        if condition.startswith("file_exists:"):
            path = Path(condition.split(":", 1)[1])
            if not path.exists():
                return False, f"file_exists:{path} — file not found"
        elif condition.startswith("file_missing:"):
            path = Path(condition.split(":", 1)[1])
            if path.exists():
                return False, f"file_missing:{path} — file exists"
        elif condition.startswith("after:"):
            required = condition.split(":", 1)[1]
            if required not in completed_this_session:
                return False, f"after:{required} — not yet completed this session"
        else:
            log.warning("Unknown condition format: %s (skipping)", condition)
    return True, "all conditions passed"


def is_schedule_due(cron_expr: str, last_run_iso: Optional[str]) -> tuple[bool, str]:
    if not cron_expr:
        return False, "no schedule (on-demand only)"
    if not CRONITER_AVAILABLE:
        return False, "croniter not installed"
    now = datetime.now(timezone.utc)
    last_run = None
    if last_run_iso:
        try:
            from dateutil.parser import parse as parse_dt
            last_run = parse_dt(last_run_iso)
        except Exception:
            pass
    try:
        cron = croniter(cron_expr, last_run or (now - timedelta(days=1)))
        next_run = cron.get_next(datetime)
        if next_run <= now:
            return True, f"cron match: {cron_expr}"
        return False, f"next run: {next_run.isoformat()}"
    except Exception as e:
        return False, f"cron error: {e}"


def evaluate_agent(
    name: str,
    config: dict,
    run_history: dict,
    completed_this_session: set[str],
    now: datetime,
) -> tuple[bool, str]:
    # Cooldown
    cooldown = int(config.get("cooldown_minutes", 60))
    last_run_iso = run_history.get(name)
    if last_run_iso and cooldown > 0:
        try:
            from dateutil.parser import parse as parse_dt
            elapsed = (now - parse_dt(last_run_iso)).total_seconds() / 60
            if elapsed < cooldown:
                return False, f"cooldown: {cooldown - elapsed:.0f} min remaining"
        except Exception:
            pass

    # Dependencies
    for dep in config.get("depends_on", []):
        if dep not in completed_this_session:
            return False, f"waiting for dependency: {dep}"

    # Conditions
    conditions = config.get("conditions", [])
    if conditions:
        passed, reason = evaluate_conditions(conditions, completed_this_session)
        if not passed:
            return False, reason

    # Schedule vs on-demand
    schedule = config.get("schedule", "")
    on_demand = config.get("on_demand", False)
    if schedule:
        due, reason = is_schedule_due(schedule, last_run_iso)
        if not due:
            return False, reason
        return True, f"scheduled: {reason}"
    if on_demand:
        return False, "on-demand only — not requested"

    return True, "always-run (no schedule restriction)"


# ── Hard Rules ─────────────────────────────────────────────────────────────

NEVER_PARALLEL = {"code_generation"}
ALWAYS_LAST    = {"deployment"}

def apply_hard_rules(ready: list[tuple[str, str]]) -> list[tuple[str, str]]:
    code_gen = [(n, r) for n, r in ready if n in NEVER_PARALLEL]
    deploy   = [(n, r) for n, r in ready if n in ALWAYS_LAST]
    others   = [(n, r) for n, r in ready if n not in NEVER_PARALLEL and n not in ALWAYS_LAST]
    return others + code_gen + deploy


# ── Human Approval Gate ────────────────────────────────────────────────────

AFFIRMATIVES = {"yes", "y", "go", "approved", "approve", "start", "ok", "sure",
                "do it", "confirm", "yep", "yeah"}
NEGATIVES    = {"no", "n", "stop", "cancel", "abort", "nope", "skip"}


def _ask_human(prompt: str) -> str:
    """Print prompt and read one line from stdin. Returns '' on EOF."""
    try:
        return input(prompt).strip().lower()
    except EOFError:
        return ""


def request_background_approval(
    session: BackgroundSession,
    agents_to_run: list[str],
    bypass: bool = False,
) -> bool:
    """
    Present a background execution plan to the human and wait for approval.
    Returns True if approved, False otherwise.
    Never starts the loop without a clear affirmative — unless bypass=True,
    in which case the gate is skipped and True is returned immediately.
    """
    # ── BYPASS MODE: skip the gate entirely ───────────────────────────────
    if bypass:
        session.approved = True
        session.bypass = True
        session.started_at = datetime.now(timezone.utc)
        end_str = session.estimated_end.strftime("%Y-%m-%d %H:%M UTC") if session.estimated_end else "unknown"
        agents_list = "\n".join(f"  ✓ {a}" for a in agents_to_run) or "  (none currently ready)"
        notice = f"""
╔══════════════════════════════════════════════════════════════╗
  RBG_Runner — BYPASS MODE ACTIVE (all approval gates skipped)
╚══════════════════════════════════════════════════════════════╝
Proceeding autonomously — no human confirmation required.

  Cycles        : {session.cycles_total}
  Interval      : every {session.interval_minutes} minute(s)
  Duration cap  : {f"{session.duration_hours}h" if session.duration_hours else "none (cycle count only)"}
  Estimated end : {end_str}
  Stop condition: cycles exhausted | duration elapsed | STOP file

Agents that will run each cycle:
{agents_list}
{'Goal: ' + session.goal if session.goal else ''}

[BYPASS] Starting background loop now.
"""
        print(notice)
        log.info("BYPASS MODE — background execution auto-approved, skipping human gate.")
        return True

    # ── Normal approval flow ───────────────────────────────────────────────
    now = datetime.now(timezone.utc)
    session.started_at = now
    end_str = session.estimated_end.strftime("%Y-%m-%d %H:%M UTC") if session.estimated_end else "unknown"

    if session.mode == "BACKGROUND_HUMAN_REQUESTED":
        header  = "Background Execution Confirmation"
        sub     = "I understood your request as:"
        approve = "Confirm?"
    else:
        header  = "Background Execution Proposal"
        sub     = "Based on the completed run, I believe repeated execution would help:"
        approve = "Approve background execution?"

    agents_list = "\n".join(f"  ✓ {a}" for a in agents_to_run) or "  (none currently ready)"

    plan = f"""
╔══════════════════════════════════════════════════════════════╗
  RBG_Runner — {header}
╚══════════════════════════════════════════════════════════════╝
{sub}

  Cycles        : {session.cycles_total}
  Interval      : every {session.interval_minutes} minute(s)
  Duration cap  : {f"{session.duration_hours}h" if session.duration_hours else "none (cycle count only)"}
  Estimated end : {end_str}
  Stop condition: cycles exhausted | duration elapsed | you type STOP

Agents that will run each cycle:
{agents_list}
{'Goal: ' + session.goal if session.goal else ''}

{approve} [yes / no]:"""

    print(plan)

    response = _ask_human("  → ")
    if response in AFFIRMATIVES:
        session.approved = True
        log.info("Background execution APPROVED by human.")
        return True
    else:
        log.info("Background execution declined or not confirmed (response: '%s').", response)
        return False


# ── Single-Cycle Execution ─────────────────────────────────────────────────

def run_single_cycle(
    workflow_agents: dict,
    run_history: dict,
    completed_this_session: set[str],
    dry_run: bool = False,
    force_agent: Optional[str] = None,
) -> tuple[dict[str, str], list[dict], list[str]]:
    """
    Execute one full pass. Returns (results, evaluated_list, selected_names).
    completed_this_session is updated in-place.
    """
    now = datetime.now(timezone.utc)
    evaluated: list[dict] = []
    results: dict[str, str] = {}

    if force_agent:
        config = workflow_agents.get(force_agent, {})
        config.setdefault("file", str(AGENTS_DIR / f"{force_agent}.md"))
        result = _invoke_agent(force_agent, config, dry_run)
        results[force_agent] = result
        if result in ("completed", "dry-run"):
            completed_this_session.add(force_agent)
            run_history[force_agent] = now.isoformat()
        return results, [{"name": force_agent, "ready": True, "reason": "force-triggered"}], [force_agent]

    ready_agents: list[tuple[str, str, int]] = []
    for name, config in workflow_agents.items():
        if name.lower() in ("rgb_runner", "rbg_runner"):
            continue
        ready, reason = evaluate_agent(name, config, run_history, completed_this_session, now)
        evaluated.append({"name": name, "ready": ready, "reason": reason})
        if ready:
            priority = int(config.get("priority", 50))
            ready_agents.append((name, reason, priority))

    ready_agents.sort(key=lambda x: x[2])
    ordered = apply_hard_rules([(n, r) for n, r, _ in ready_agents])
    selected = [n for n, _ in ordered]

    for name, _ in ordered:
        config = workflow_agents.get(name, {})
        config.setdefault("file", str(AGENTS_DIR / f"{name}.md"))
        unmet_deps = [d for d in config.get("depends_on", []) if d not in completed_this_session]
        if unmet_deps:
            results[name] = f"skipped (unmet deps: {unmet_deps})"
            continue
        result = _invoke_agent(name, config, dry_run)
        results[name] = result
        if result in ("completed", "dry-run"):
            completed_this_session.add(name)
            if not dry_run:
                run_history[name] = now.isoformat()

    return results, evaluated, selected


def _invoke_agent(name: str, config: dict, dry_run: bool) -> str:
    """
    Hook: trigger one agent. Replace the body of this function with your
    actual OpenCode CLI invocation.

    Example using the opencode CLI:
        import subprocess
        result = subprocess.run(
            ["opencode", "run", "--agent", name],
            capture_output=True, text=True, timeout=300
        )
        return "completed" if result.returncode == 0 else "failed"
    """
    if dry_run:
        log.info("[DRY-RUN] Would trigger: %s (%s)", name, config.get("file", ""))
        return "dry-run"
    log.info("Triggering agent: %s", name)
    # ↓ Replace this stub with your real invocation ↓
    log.info("  (stub — wire your OpenCode CLI call here)")
    return "completed"


# ── Background Loop ────────────────────────────────────────────────────────

def run_background_loop(
    session: BackgroundSession,
    workflow_agents: dict,
    run_history: dict,
    dry_run: bool = False,
) -> None:
    """
    Execute repeated cycles with sleep intervals between them.
    Checks for a STOP file (.opencode/memory/STOP) between cycles as an
    out-of-band human interrupt mechanism.
    """
    STOP_FILE = OPENCODE_INTERNAL / "memory" / "STOP"
    session.started_at = datetime.now(timezone.utc)
    completed_this_session: set[str] = set()

    log.info(
        "Background loop starting: %d cycles × %d min interval%s",
        session.cycles_total, session.interval_minutes,
        " [BYPASS MODE]" if session.bypass else "",
    )
    print(f"\n[RBG_Runner] Background session started. "
          f"Type STOP in a file at {STOP_FILE} to interrupt between cycles.\n")

    all_results: list[dict] = []

    while not session.stop_condition_reached:
        cycle_num = session.cycles_completed + 1
        log.info("── Cycle %d / %d ──", cycle_num, session.cycles_total)

        results, evaluated, selected = run_single_cycle(
            workflow_agents, run_history, completed_this_session, dry_run
        )
        session.cycles_completed += 1

        if not dry_run:
            save_run_history(run_history)

        all_results.append({
            "cycle": cycle_num,
            "results": results,
            "selected": selected,
        })

        _append_cycle_log(session, cycle_num, evaluated, results)

        if session.stop_condition_reached:
            break

        # Check for human STOP signal between cycles
        if STOP_FILE.exists():
            log.info("STOP file detected — exiting background loop.")
            try:
                STOP_FILE.unlink()
            except OSError:
                pass
            break

        sleep_secs = session.interval_minutes * 60
        next_cycle_at = datetime.now(timezone.utc) + timedelta(seconds=sleep_secs)
        log.info("Sleeping %d min until next cycle at %s UTC",
                 session.interval_minutes,
                 next_cycle_at.strftime("%H:%M:%S"))
        if not dry_run:
            time.sleep(sleep_secs)
        else:
            log.info("[DRY-RUN] Skipping sleep.")
            break   # don't loop infinitely in dry-run mode

    _append_session_summary(session, all_results)
    log.info(
        "Background session complete: %d / %d cycles completed.",
        session.cycles_completed, session.cycles_total,
    )


# ── Logging ────────────────────────────────────────────────────────────────

def _append_cycle_log(
    session: BackgroundSession,
    cycle_num: int,
    evaluated: list[dict],
    results: dict[str, str],
) -> None:
    RUNNER_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    evaluated_lines = "\n".join(
        f"  - {e['name']}: {'✓' if e['ready'] else '✗'} — {e['reason']}"
        for e in evaluated
    )
    result_lines = "\n".join(f"  - {k}: {v}" for k, v in results.items()) or "  (none)"
    bypass_tag = " [BYPASS]" if getattr(session, "bypass", False) else ""
    entry = (
        f"\n## [{ts}] RBG_Runner — "
        f"{'Cycle ' + str(cycle_num) + '/' + str(session.cycles_total) if session.cycles_total > 1 else 'Single Run'}"
        f" ({session.mode}{bypass_tag})\n"
        f"- **Agents evaluated**:\n{evaluated_lines}\n"
        f"- **Results**:\n{result_lines}\n"
    )
    with open(RUNNER_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)


def _append_session_summary(session: BackgroundSession, all_results: list[dict]) -> None:
    RUNNER_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_agents = sum(len(r["results"]) for r in all_results)
    duration_str = ""
    if session.started_at:
        elapsed = datetime.now(timezone.utc) - session.started_at
        h, rem = divmod(int(elapsed.total_seconds()), 3600)
        m = rem // 60
        duration_str = f"{h}h {m}m"
    bypass_note = " (bypass mode — no human approval required)" if getattr(session, "bypass", False) else ""
    entry = (
        f"\n## [{ts}] Background Session Complete\n"
        f"- **Mode**: {session.mode}{bypass_note}\n"
        f"- **Cycles completed**: {session.cycles_completed} / {session.cycles_total}\n"
        f"- **Duration**: {duration_str}\n"
        f"- **Total agent invocations**: {total_agents}\n"
        f"- **Stop reason**: "
        + ("cycles exhausted" if session.cycles_completed >= session.cycles_total else "duration elapsed or interrupted")
        + "\n"
    )
    with open(RUNNER_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)


# ── Main Orchestration ─────────────────────────────────────────────────────

def orchestrate(args: argparse.Namespace) -> None:
    """Top-level entry point. Determines mode and dispatches accordingly."""

    bypass = getattr(args, "bypass", False)

    # Safety: unattended runs are always SINGLE — no approval possible.
    # bypass + unattended is a contradiction; unattended wins for safety.
    if args.unattended and (args.cycles > 1 or args.propose_background):
        log.info("Unattended mode — falling back to SINGLE RUN (no approval possible).")
        args.cycles = 1
        args.propose_background = False
        bypass = False  # unattended overrides bypass for safety

    if bypass:
        log.info("BYPASS MODE active — all human approval gates will be skipped this session.")

    agents_registry = discover_agents(AGENTS_DIR)
    workflow        = load_workflow(WORKFLOW_FILE)
    workflow_agents = workflow.get("agents", {})
    run_history     = load_run_history()
    completed: set[str] = set()

    # ── MODE 2: BACKGROUND_HUMAN_REQUESTED ────────────────────────────────
    if args.cycles > 1:
        session = BackgroundSession(
            cycles_total=args.cycles,
            interval_minutes=args.interval,
            duration_hours=args.duration,
            goal=args.goal,
            mode="BACKGROUND_HUMAN_REQUESTED",
        )
        # Determine which agents would run in cycle 1
        now = datetime.now(timezone.utc)
        agents_to_run = [
            name for name, config in workflow_agents.items()
            if name.lower() not in ("rgb_runner", "rbg_runner")
            and evaluate_agent(name, config, run_history, set(), now)[0]
        ]
        approved = request_background_approval(session, agents_to_run, bypass=bypass)
        if not approved:
            log.info("Approval not given — falling back to SINGLE RUN.")
            _run_single_and_report(workflow_agents, run_history, completed, args, "SINGLE")
            return
        run_background_loop(session, workflow_agents, run_history, args.dry_run)
        return

    # ── MODE 3: BACKGROUND_PROPOSED ───────────────────────────────────────
    if args.propose_background:
        # Step 1: complete one full single run
        log.info("BACKGROUND_PROPOSED mode — completing one full run first.")
        results, evaluated, selected = run_single_cycle(
            workflow_agents, run_history, completed, args.dry_run, args.agent
        )
        if not args.dry_run:
            save_run_history(run_history)
        _append_cycle_log(
            BackgroundSession(1, 0, None, mode="SINGLE"),
            1, evaluated, results
        )
        _print_report("BACKGROUND_PROPOSED_ASSESSMENT", results, evaluated, selected, None)

        # Step 2: assess whether looping adds value
        completed_count = sum(1 for v in results.values() if v == "completed")
        if completed_count == 0:
            log.info("No agents completed — background proposal skipped.")
            return

        # Build a sensible default proposal (user can customise at the prompt)
        proposed_session = BackgroundSession(
            cycles_total=5,
            interval_minutes=60,
            duration_hours=5.0,
            goal=args.goal or "continue iterating on the agents' outputs",
            mode="BACKGROUND_PROPOSED",
        )
        agents_ran = list(results.keys())
        approved = request_background_approval(proposed_session, agents_ran, bypass=bypass)
        if not approved:
            log.info("Background proposal declined — stopping after single run.")
            return
        run_background_loop(proposed_session, workflow_agents, run_history, args.dry_run)
        return

    # ── BYPASS + no explicit schedule: auto-escalate to background ────────
    # When bypass mode is on but no explicit schedule was given, the agent
    # decides autonomously whether a background run makes sense. Default
    # to a sensible 3-cycle / 60-min schedule rather than silently doing
    # a single run and exiting.
    if bypass and args.cycles == 1 and not args.propose_background:
        log.info("BYPASS MODE + no explicit schedule — auto-proposing background run (3 cycles, 60 min).")
        auto_session = BackgroundSession(
            cycles_total=3,
            interval_minutes=60,
            duration_hours=3.0,
            goal=args.goal or "autonomous background pass",
            mode="BACKGROUND_HUMAN_REQUESTED",
        )
        now = datetime.now(timezone.utc)
        agents_to_run = [
            name for name, config in workflow_agents.items()
            if name.lower() not in ("rgb_runner", "rbg_runner")
            and evaluate_agent(name, config, run_history, set(), now)[0]
        ]
        # Bypass auto-approves; no human prompt shown
        request_background_approval(auto_session, agents_to_run, bypass=True)
        run_background_loop(auto_session, workflow_agents, run_history, args.dry_run)
        return

    # ── MODE 1: SINGLE RUN ────────────────────────────────────────────────
    _run_single_and_report(workflow_agents, run_history, completed, args, "SINGLE")


def _run_single_and_report(
    workflow_agents: dict,
    run_history: dict,
    completed: set[str],
    args: argparse.Namespace,
    mode: str,
) -> None:
    results, evaluated, selected = run_single_cycle(
        workflow_agents, run_history, completed, args.dry_run,
        getattr(args, "agent", None)
    )
    if not args.dry_run:
        save_run_history(run_history)
    _append_cycle_log(BackgroundSession(1, 0, None, mode=mode), 1, evaluated, results)
    _print_report(mode, results, evaluated, selected, None)


def _print_report(
    mode: str,
    results: dict[str, str],
    evaluated: list[dict],
    selected: list[str],
    session: Optional[BackgroundSession],
) -> None:
    report = {
        "runner_session": datetime.now(timezone.utc).isoformat(),
        "execution_mode": mode,
        "bypass_mode": getattr(session, "bypass", False) if session else False,
        "background_session": (
            {
                "approved": session.approved,
                "bypass": session.bypass,
                "cycles_total": session.cycles_total,
                "cycles_completed": session.cycles_completed,
                "interval_minutes": session.interval_minutes,
                "duration_hours": session.duration_hours,
                "estimated_end": session.estimated_end.isoformat() if session.estimated_end else None,
            }
            if session else None
        ),
        "agents_evaluated": evaluated,
        "agents_selected": selected,
        "results": results,
    }
    print("\n" + "=" * 60)
    print("RBG_Runner Run Report")
    print("=" * 60)
    print(json.dumps(report, indent=2, default=str))


# ── CLI ────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="RBG_Runner — Intelligent Agent Orchestrator for oc-toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Execution modes:
  SINGLE (default)             Run all ready agents once, then exit.
  BACKGROUND_HUMAN_REQUESTED   --cycles N  [--interval M] [--duration H]
  BACKGROUND_PROPOSED          --propose-background
  BYPASS MODE                  --bypass  (skips all approval gates; agent decides autonomously)

Background loops require human approval at the terminal (unless --bypass is set).
Use --unattended with cron/Task Scheduler to guarantee SINGLE RUN.

Examples:
  python rgb_runner.py --cycles 10 --interval 60
      → propose background: 10 runs, 1 per hour (asks for approval)

  python rgb_runner.py --cycles 5 --interval 30 --duration 3 --goal "review all emails"
      → background with duration cap and a stated goal

  python rgb_runner.py --propose-background
      → run once, then propose looping if it would help

  python rgb_runner.py --bypass
      → bypass mode: agent decides autonomously (default: 3 cycles, 60 min interval)

  python rgb_runner.py --bypass --cycles 10 --interval 30
      → bypass mode with explicit schedule (no confirmation prompt)

  python rgb_runner.py --unattended --trigger scheduled
      → safe for cron: always single run, no interactive prompt
""",
    )

    # Single-run / force
    parser.add_argument("--agent", metavar="NAME",
                        help="Force-trigger one specific agent (skips schedule/cooldown checks)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show which agents would run without triggering them")
    parser.add_argument("--trigger", default="on-demand",
                        choices=["on-demand", "scheduled", "condition-met"],
                        help="Declare what caused this run (for logging)")

    # Background mode
    parser.add_argument("--cycles", type=int, default=1, metavar="N",
                        help="Number of background cycles to run (>1 → BACKGROUND mode, asks for approval)")
    parser.add_argument("--interval", type=int, default=60, metavar="MINUTES",
                        help="Minutes to sleep between background cycles (default: 60)")
    parser.add_argument("--duration", type=float, default=None, metavar="HOURS",
                        help="Optional wall-clock duration cap for background runs (hours)")
    parser.add_argument("--goal", default="", metavar="TEXT",
                        help="Human-readable goal shown in the approval prompt")
    parser.add_argument("--propose-background", action="store_true",
                        help="Run once, then propose background execution if more cycles would help")

    # Bypass mode
    parser.add_argument("--bypass", action="store_true",
                        help=(
                            "Bypass all human approval gates. The agent decides autonomously "
                            "on cycles/interval/mode and proceeds without confirmation. "
                            "Session-scoped only. Everything is still logged to runner_log.md."
                        ))

    # Safety
    parser.add_argument("--unattended", action="store_true",
                        help="Unattended / cron mode — always SINGLE RUN, never shows approval prompt")

    # Utility
    parser.add_argument("--list", action="store_true",
                        help="List all agents and their current readiness")
    parser.add_argument("--init", action="store_true",
                        help="Scaffold workflow.json from the agents/ directory")

    args = parser.parse_args()

    if args.init:
        if WORKFLOW_FILE.exists():
            print(f"workflow.json already exists at {WORKFLOW_FILE}. Delete it first to re-scaffold.")
            sys.exit(1)
        registry = discover_agents(AGENTS_DIR)
        scaffold_workflow(registry, WORKFLOW_FILE)
        sys.exit(0)

    if args.list:
        registry = discover_agents(AGENTS_DIR)
        workflow  = load_workflow(WORKFLOW_FILE)
        run_history = load_run_history()
        now = datetime.now(timezone.utc)
        completed: set[str] = set()
        print(f"\n{'Agent':<30} {'Mode':<12} {'Schedule':<22} {'Ready':<8} {'Last Run'}")
        print("-" * 90)
        for name, meta in sorted(registry.items()):
            config  = workflow.get("agents", {}).get(name, {})
            schedule = config.get("schedule", "on-demand")
            ready, reason = evaluate_agent(name, config, run_history, completed, now)
            last_run = run_history.get(name, "never")
            ready_str = "✓ yes" if ready else "✗ no"
            print(f"{name:<30} {meta.get('mode','?'):<12} {schedule:<22} {ready_str:<8} {last_run}")
        print()
        sys.exit(0)

    orchestrate(args)


if __name__ == "__main__":
    main()
