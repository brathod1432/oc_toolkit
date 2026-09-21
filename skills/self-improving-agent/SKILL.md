---
name: "self-improving-agent"
description: "Curate an agent runtime's auto-memory into durable project knowledge. Analyze MEMORY.md for patterns, promote proven learnings to AI_RUNTIME_GUIDE.md and .claude/rules/, extract recurring solutions into reusable skills. Use when: (1) reviewing what AI assistant has learned about your project, (2) graduating a pattern from notes to enforced rules, (3) turning a debugging solution into a skill, (4) checking memory health and capacity."
---

## Internal Safety Override

- Status: local-only unless explicitly opted into external access.
- Before using network tools, account connectors, browser automation, or APIs, state the destination, data scope, and credential source.
- Do not transmit repository files, secrets, credentials, or private documents by default.
- Audit categories: network, secrets.

# Self-Improving Agent

> Auto-memory captures. This plugin curates.

an agent runtime's auto-memory (v2.1.32+) automatically records project patterns, debugging insights, and your preferences in `MEMORY.md`. This plugin adds the intelligence layer: it analyzes what AI assistant has learned, promotes proven patterns into project rules, and extracts recurring solutions into reusable skills.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/si:review` | Analyze MEMORY.md â€” find promotion candidates, stale entries, consolidation opportunities |
| `/si:promote` | Graduate a pattern from MEMORY.md â†’ AI_RUNTIME_GUIDE.md or `.claude/rules/` |
| `/si:extract` | Turn a proven pattern into a standalone skill |
| `/si:status` | Memory health dashboard â€” line counts, topic files, recommendations |
| `/si:remember` | Explicitly save important knowledge to auto-memory |

## How It Fits Together

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                  an agent runtime Memory Stack                â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚  AI_RUNTIME_GUIDE.md  â”‚   Auto Memory    â”‚   Session Memory       â”‚
â”‚  (you write)â”‚   (AI assistant writes)â”‚   (AI assistant writes)      â”‚
â”‚  Rules &    â”‚   MEMORY.md      â”‚   Conversation logs    â”‚
â”‚  standards  â”‚   + topic files  â”‚   + continuity         â”‚
â”‚  Full load  â”‚   First 200 linesâ”‚   Contextual load      â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚              â†‘ /si:promote        â†‘ /si:review          â”‚
â”‚         Self-Improving Agent (this plugin)               â”‚
â”‚              â†“ /si:extract    â†“ /si:remember            â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚  .claude/rules/    â”‚    New Skills    â”‚   Error Logs     â”‚
â”‚  (scoped rules)    â”‚    (extracted)   â”‚   (auto-captured)â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

## Installation

### an agent runtime (Plugin)
```
/plugin marketplace add alirezarezvani/ai-ops-skills
/plugin install self-improving-agent@ai-ops-skills
```

### OpenClaw
```bash
clawhub install self-improving-agent
```

### an agent runtime
```bash
./scripts/codex-install.sh --skill self-improving-agent
```

## Memory Architecture

### Where things live

| File | Who writes | Scope | Loaded |
|------|-----------|-------|--------|
| `./AI_RUNTIME_GUIDE.md` | You (+ `/si:promote`) | Project rules | Full file, every session |
| `~/.claude/AI_RUNTIME_GUIDE.md` | You | Global preferences | Full file, every session |
| `~/.claude/projects/<path>/memory/MEMORY.md` | AI assistant (auto) | Project learnings | First 200 lines |
| `~/.claude/projects/<path>/memory/*.md` | AI assistant (overflow) | Topic-specific notes | On demand |
| `.claude/rules/*.md` | You (+ `/si:promote`) | Scoped rules | When matching files open |

### The promotion lifecycle

```
1. AI assistant discovers pattern â†’ auto-memory (MEMORY.md)
2. Pattern recurs 2-3x â†’ /si:review flags it as promotion candidate
3. You approve â†’ /si:promote graduates it to AI_RUNTIME_GUIDE.md or rules/
4. Pattern becomes an enforced rule, not just a note
5. MEMORY.md entry removed â†’ frees space for new learnings
```

## Core Concepts

### Auto-memory is capture, not curation

Auto-memory is excellent at recording what AI assistant learns. But it has no judgment about:
- Which learnings are temporary vs. permanent
- Which patterns should become enforced rules
- When the 200-line limit is wasting space on stale entries
- Which solutions are good enough to become reusable skills

That's what this plugin does.

### Promotion = graduation

When you promote a learning, it moves from AI assistant's scratchpad (MEMORY.md) to your project's rule system (AI_RUNTIME_GUIDE.md or `.claude/rules/`). The difference matters:

- **MEMORY.md**: "I noticed this project uses pnpm" (background context)
- **AI_RUNTIME_GUIDE.md**: "Use pnpm, not npm" (enforced instruction)

Promoted rules have higher priority and load in full (not truncated at 200 lines).

### Rules directory for scoped knowledge

Not everything belongs in AI_RUNTIME_GUIDE.md. Use `.claude/rules/` for patterns that only apply to specific file types:

```yaml
# .claude/rules/api-testing.md
---
paths:
  - "src/api/**/*.test.ts"
  - "tests/api/**/*"
---
- Use supertest for API endpoint testing
- Mock external services with msw
- Always test error responses, not just happy paths
```

This loads only when AI assistant works with API test files â€” zero overhead otherwise.

## Agents

### memory-analyst
Analyzes MEMORY.md and topic files to identify:
- Entries that recur across sessions (promotion candidates)
- Stale entries referencing deleted files or old patterns
- Related entries that should be consolidated
- Gaps between what MEMORY.md knows and what AI_RUNTIME_GUIDE.md enforces

### skill-extractor
Takes a proven pattern and generates a complete skill:
- SKILL.md with proper frontmatter
- Reference documentation
- Examples and edge cases
- Ready for `/plugin install` or `clawhub publish`

## Hooks

### error-capture (PostToolUse â†’ Bash)
Monitors command output for errors. When detected, appends a structured entry to auto-memory with:
- The command that failed
- Error output (truncated)
- Timestamp and context
- Suggested category

**Token overhead:** Zero on success. ~30 tokens only when an error is detected.

## Platform Support

| Platform | Memory System | Plugin Works? |
|----------|--------------|---------------|
| an agent runtime | Auto-memory (MEMORY.md) | âœ… Full support |
| OpenClaw | workspace/MEMORY.md | âœ… Adapted (reads workspace memory) |
| an agent runtime | AGENTS.md | âœ… Adapted (reads AGENTS.md patterns) |
| GitHub Copilot | `.github/copilot-instructions.md` | âš ï¸ Manual promotion only |

## Related

- [an agent runtime Memory Docs](https://code.claude.com/docs/en/memory)
- [pskoett/self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent) â€” inspiration
- [playwright-pro](../playwright-pro/) â€” sister plugin in this repo
