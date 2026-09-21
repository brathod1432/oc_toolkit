# Workflow Rules

These rules govern how every opencode session runs, regardless of which agent is active.

---

## Session Start Checklist

Before doing ANY work in a project directory:

1. **Check for `RBG_README.md`** at the project root
   - If found → read it completely before touching anything else
   - If missing → ask "Is this a new project? Should I initialise RBG_* files?"
2. **Check for `.opencode/rules/rules.md`** — read it; it overrides global rules
3. **Check `RBG_todo.md`** — note any open backlog items relevant to the request

Do not skip step 1. It is never optional.

---

## Task Lifecycle

Every non-trivial task follows this lifecycle:

```
PLANNING → (approval) → IMPLEMENTATION → TEST×3 → SUMMARY
```

For quick single-file tasks, still log a one-line entry to `RBG_changelog.md`.

### Standard phases when using brijesh-dev:

| Phase | What happens |
|---|---|
| PLANNING | Idea Planner + Business Planner produce a task plan |
| PLAN REVIEW | Human approval gate (unless bypass mode) |
| IMPLEMENTATION | Code Generator builds; other agents contribute |
| IMPL REVIEW | Human reviews diff (unless bypass mode) |
| TEST CYCLE 1-3 | pytest runs; bugs fixed between cycles |
| FINAL SUMMARY | RBG_README.md updated; RBG_changelog.md appended |

### Bypass mode triggers (no approval gates):

Any of: "decide the best", "just do it", "your call", "you decide",
"bypass", "no approval", "skip approval", "auto", "autonomous",
"just decide", "don't ask me"

---

## Changelog Protocol

Every task — even tiny ones — appends to `RBG_changelog.md`:

```markdown
## [YYYY-MM-DD HH:MM] <task-id> — <one-line summary>
- PHASE: <what happened>
- AGENTS: <which agents ran>
- OUTCOME: <result / PR / file changed>
```

Never overwrite. Only append.

---

## Agent Selection Guide

| Task type | Use |
|---|---|
| "Build X from scratch" | brijesh-dev (full cycle) |
| "Quick fix in file Y" | 08_code_generation directly |
| "Write tweet/post" | 05_social_media directly |
| "What should we charge?" | 03_business_planning → 10_finance |
| "Who are our competitors?" | 04_competitor_research |
| "Write cold email" | 07_email_outreach |
| "Reply to support ticket" | 09_customer_support |
| "Deploy to Render" | 11_deployment |
| "Run Google Ads" | 06_ads_management |

Use `brijesh-dev` for anything that spans multiple agents or multiple phases.

---

## Output Conventions

- Always show the file path before any code block
- Diffs over full rewrites — preserve existing code where possible
- When creating new files, also update `RBG_todo.md` if follow-up tasks exist
- Never commit secrets, `.env`, or `.opencode/` to git
