# Rules Directory Patterns

Best practices for organizing `.claude/rules/` files â€” the scoped instruction system that loads rules only when relevant files are open.

## Directory Structure

```
.claude/
â”œâ”€â”€ AI_RUNTIME_GUIDE.md              # Main project instructions (always loaded)
â””â”€â”€ rules/
    â”œâ”€â”€ code-style.md      # No paths â†’ loads always (like AI_RUNTIME_GUIDE.md)
    â”œâ”€â”€ testing.md          # Scoped to test files
    â”œâ”€â”€ api-design.md       # Scoped to API source files
    â”œâ”€â”€ database.md         # Scoped to migration/model files
    â””â”€â”€ frontend/
        â”œâ”€â”€ components.md   # Scoped to React components
        â””â”€â”€ styling.md      # Scoped to CSS/styled files
```

## Path Scoping

### Basic patterns

```yaml
---
paths:
  - "**/*.test.ts"              # All TypeScript test files
  - "src/api/**/*.ts"           # API source files
  - "*.md"                      # Root-level markdown
  - "src/components/**/*.tsx"   # React components
---
```

### Brace expansion

```yaml
---
paths:
  - "src/**/*.{ts,tsx}"         # All TypeScript + TSX
  - "tests/**/*.{test,spec}.ts" # Test and spec files
---
```

### Multiple scopes

```yaml
---
paths:
  - "src/api/**/*.ts"
  - "tests/api/**/*"
  - "openapi.yaml"
---
```

## Common Rule Files

### testing.md
```yaml
---
paths:
  - "**/*.test.{ts,tsx,js,jsx}"
  - "**/*.spec.{ts,tsx,js,jsx}"
  - "tests/**/*"
  - "__tests__/**/*"
---

# Testing Rules

- Use `describe` blocks to group related tests
- One assertion per test when possible
- Mock external services; never hit real APIs in tests
- Use factories for test data, not inline objects
- Run `pnpm test` before committing
```

### api-design.md
```yaml
---
paths:
  - "src/api/**/*.ts"
  - "src/routes/**/*.ts"
  - "src/handlers/**/*.ts"
---

# API Design Rules

- Validate all input with Zod schemas
- Use `ApiError` class for error responses
- Include OpenAPI JSDoc on all handlers
- Return consistent error format: `{ error: string, code: string }`
```

### database.md
```yaml
---
paths:
  - "src/db/**/*"
  - "migrations/**/*"
  - "prisma/**/*"
  - "drizzle/**/*"
---

# Database Rules

- Always create a migration for schema changes
- Never modify existing migrations â€” create new ones
- Use transactions for multi-table operations
- Index foreign keys and frequently queried columns
```

### security.md (unscoped â€” always loads)
```markdown
# Security Rules

- Never log sensitive data (tokens, passwords, PII)
- Sanitize all user input before database queries
- Use parameterized queries, never string interpolation
- Validate file uploads: type, size, content
- Environment variables for all secrets â€” never hardcode
```

## When to Create a Rule File

| Signal | Action |
|--------|--------|
| AI_RUNTIME_GUIDE.md over 150 lines | Move scoped patterns to rules/ |
| Same instruction repeated for different file types | Create a scoped rule |
| `/si:promote` suggests a file-type-specific pattern | Create or append to a rule file |
| Team adds a new convention for a specific area | New rule file |

## Organization Tips

1. **One topic per file** â€” `testing.md`, not `testing-and-linting.md`
2. **Use subdirectories for large projects** â€” `rules/frontend/`, `rules/backend/`
3. **Keep unscoped rules minimal** â€” they load every session like AI_RUNTIME_GUIDE.md
4. **Review after refactors** â€” paths may change when directories are reorganized
5. **Share via git** â€” rules/ should be version-controlled (unlike auto-memory)
