# an agent runtime Memory Architecture

A complete reference for how an agent runtime's memory systems work together.

## Three Memory Systems

### 1. AI_RUNTIME_GUIDE.md Files (You â†’ AI assistant)

**Purpose:** Persistent instructions you write to guide AI assistant's behavior.

**Locations (in priority order):**
| Scope | Path | Shared |
|-------|------|--------|
| Managed policy | `/etc/claude-code/AI_RUNTIME_GUIDE.md` (Linux) | All users |
| Project | `./AI_RUNTIME_GUIDE.md` or `./.claude/AI_RUNTIME_GUIDE.md` | Team (git) |
| User | `~/.claude/AI_RUNTIME_GUIDE.md` | Just you |
| Local | `./CLAUDE.local.md` | Just you |

**Loading:** Full file, every session. Files higher in the directory tree load first.

**Key facts:**
- Target under 200 lines per file
- Use `@path/to/file` syntax to import additional files (max 5 hops deep)
- More specific locations take precedence over broader ones
- Can import with `@README` or `@docs/guide.md`
- CLAUDE.local.md is auto-added to .gitignore

### 2. Auto Memory (AI assistant â†’ AI assistant)

**Purpose:** Notes AI assistant writes to itself about project patterns and learnings.

**Location:** `~/.claude/projects/<project-path>/memory/`

**Structure:**
```
~/.claude/projects/<project-path>/memory/
â”œâ”€â”€ MEMORY.md           # Main file (first 200 lines loaded)
â”œâ”€â”€ debugging.md        # Topic file (loaded on demand)
â”œâ”€â”€ patterns.md         # Topic file (loaded on demand)
â””â”€â”€ ...                 # More topic files as needed
```

**Key facts:**
- Enabled by default (since v2.1.32)
- Only the first 200 lines of MEMORY.md load at startup
- AI assistant creates topic files automatically when MEMORY.md gets long
- Git repo root determines the project path
- Git worktrees get separate memory directories
- Local only â€” not shared via git
- Toggle with `/memory`, settings, or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`
- Subagents can have their own auto memory

**What it captures:**
- Build commands and test conventions
- Debugging solutions and error patterns
- Code style preferences and architecture notes
- Your communication preferences and workflow habits

### 3. Session Memory (AI assistant â†’ AI assistant)

**Purpose:** Conversation summaries for cross-session continuity.

**Location:** `~/.claude/projects/<project-path>/<session>/session-memory/`

**Key facts:**
- Saves what was discussed and decided in specific sessions
- "What did we do yesterday?" context
- Loaded contextually (relevant past sessions, not all)
- Use `/remember` to turn session memory into permanent project knowledge

### 4. Rules Directory (You â†’ AI assistant, scoped)

**Purpose:** Modular instructions scoped to specific file types.

**Location:** `.claude/rules/*.md`

**Key facts:**
- Uses YAML frontmatter with `paths` field for scoping
- Only loads when AI assistant works with matching files
- Recursive â€” can organize into subdirectories
- Same priority as `.claude/AI_RUNTIME_GUIDE.md`
- Great for keeping AI_RUNTIME_GUIDE.md under 200 lines

```yaml
---
paths:
  - "src/api/**/*.ts"
---
# API rules only load when working with API files
```

## Memory Priority

When entries conflict:

1. AI_RUNTIME_GUIDE.md (highest â€” explicit instructions)
2. `.claude/rules/` (high â€” scoped instructions)
3. Auto-memory MEMORY.md (medium â€” learned patterns)
4. Session memory (low â€” historical context)

## The Self-Improving Agent's Role

```
Auto-memory captures â†’ This plugin curates â†’ AI_RUNTIME_GUIDE.md enforces

MEMORY.md (raw notes)  â†’  /si:review (analyze)  â†’  /si:promote (graduate)
                                                          â†“
                                                    AI_RUNTIME_GUIDE.md or
                                                    .claude/rules/
                                                    (enforced rules)
```

**Why this matters:** MEMORY.md entries are background context truncated at 200 lines. AI_RUNTIME_GUIDE.md entries are high-priority instructions loaded in full. Promoting a pattern from memory to rules fundamentally changes how AI assistant treats it.

## Capacity Planning

| File | Soft limit | Hard limit | What happens at limit |
|------|-----------|------------|----------------------|
| MEMORY.md | 150 lines | 200 lines | Lines after 200 not loaded at startup |
| AI_RUNTIME_GUIDE.md | 150 lines | No hard limit | Adherence decreases with length |
| Topic files | No limit | No limit | Loaded on demand, not at startup |
| Rules files | No limit per file | No limit | Only loaded when paths match |

## Best Practices

1. **Keep MEMORY.md lean** â€” promote proven patterns, delete stale ones
2. **Keep AI_RUNTIME_GUIDE.md under 200 lines** â€” split into rules/ if growing
3. **Don't duplicate** â€” if it's in AI_RUNTIME_GUIDE.md, remove it from MEMORY.md
4. **Scope rules** â€” use `.claude/rules/` with paths for file-type-specific patterns
5. **Review quarterly** â€” memory files go stale after refactors
6. **Use /si:status** â€” monitor capacity before it becomes a problem
