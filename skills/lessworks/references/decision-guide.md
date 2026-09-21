# LessWorks Decision Guide

Quick reference for choosing the right mode, applying the ladder, and handling common scenarios.

---

## Mode Selection — Pick in Under 5 Seconds

| Situation | Mode |
|---|---|
| Normal task, no special instruction | `full` (always active) |
| "Quick fix", "just change X", "one-liner" | `lite` |
| Touching shared utilities, models, or services used by many callers | `strict` |
| Auth, payments, migrations, production config, CI/CD | `intense` |
| "Review this", "is this over-engineered?", "find bloat" | `audit` |
| User explicitly asks for comprehensive design/exploration | `off` |
| User says "LessWorks off" or "no LessWorks" | `off` |

---

## The Ladder — Applied to This Stack

Walk top to bottom. Stop at the first step that safely solves the problem.

```
PYTHON / FASTAPI / NVIDIA CONTEXT

Step 1: Should this exist?
         → If adding a new endpoint: does one already exist that handles this case?
         → If adding a new model: is there already a SQLAlchemy model that covers it?

Step 2: Can it be deleted instead?
         → Is there dead code, a duplicate route, or an unused schema that should go?

Step 3: Is this already in the codebase?
         → Search existing routers, crud.py, schemas, utils/ before writing anything
         → grep/read the relevant module first

Step 4: Reuse existing function/pattern?
         → Existing CRUD helper? Add a parameter rather than a new function
         → Existing Pydantic schema? Extend it or use Optional fields

Step 5: Standard library?
         → uuid.uuid4()  not shortuuid or nanoid
         → pathlib.Path  not os.path
         → json          not simplejson or orjson (unless already installed)
         → datetime      not arrow or pendulum (unless already installed)
         → logging       not loguru (unless already installed)
         → asyncio       not trio or anyio (unless already installed)

Step 6: Native platform?
         → FastAPI's built-in Depends() over a custom DI container
         → FastAPI's HTTPException over a custom error class (unless project has one)
         → Pydantic's built-in validators over custom __validators__
         → SQLAlchemy's async session over raw connections

Step 7: Already-installed dependency?
         → Check requirements.txt / pyproject.toml BEFORE importing anything
         → httpx (already in FastAPI projects) for NVIDIA API calls — not requests
         → pytest + httpx (AsyncClient) for async route tests — not aiohttp test utils

Step 8: One-line or small local change?
         → Add a field to an existing schema
         → Add a condition to an existing route
         → Add a parameter to an existing crud function

Step 9: New code — only if steps 1–8 fail
         → New function in the appropriate existing module
         → New schema in schemas.py
         → No new file unless the module would exceed ~300 lines

Step 10: New dependency or abstraction — ONLY with explicit user approval
          → State: why stdlib is insufficient, why existing deps fail,
            security/maintenance risk, exact package name and version pin
```

---

## Scenario → Action Table

| Request | LessWorks Action |
|---|---|
| "Add a /health endpoint" | Check if one exists; if not, 3-line route in main.py or appropriate router |
| "Add X field to the User model" | Add field to SQLAlchemy model + Pydantic schema; run migration; do not rename existing fields |
| "Fix this 422 error" | Read the route, inspect the Pydantic schema, find the mismatch; patch the schema or the caller |
| "Add NVIDIA API call for feature X" | Use httpx (already installed); reuse existing NVIDIA client pattern if one exists in the project |
| "We need better logging" | Add `logging.getLogger(__name__)` to the affected module; do not install loguru unless it's in requirements.txt |
| "Refactor this file" | Only if current task requires it; delete duplication; do not reorganize unrelated logic |
| "Add authentication" | **INTENSE MODE** — auth is high-risk; inspect existing auth patterns first, get explicit approval |
| "Add a new agent" | Check existing agent files for a similar agent; copy the minimum diff; do not create a new base class unless 3+ agents share identical logic |
| "Install package X" | Check if it's in requirements.txt; if not, ask for explicit approval before touching dependency files |
| "Add tests" | One happy path + one error case + one edge case for the changed behavior; do not write a full test suite for untouched code |
| "Add a database migration" | **INTENSE MODE** — inspect existing migration files, check column types, always add a rollback note |

---

## Risk Matrix

Use this to decide between `full`, `strict`, and `intense`.

| Code Area | Risk | Recommended Mode |
|---|---|---|
| New read-only GET route | Low | full |
| New POST route with validation | Low–Medium | full |
| Existing route modified | Medium | strict |
| Shared utility function modified | Medium | strict |
| CRUD function that affects multiple models | Medium–High | strict |
| Auth middleware or JWT handling | High | intense |
| Payment or billing logic | High | intense + explicit approval |
| Database schema change / migration | High | intense + explicit approval |
| Environment variable / secrets handling | High | intense + explicit approval |
| NVIDIA API key usage | High | intense — never log or expose key |
| Production Render config or Dockerfile | High | intense + explicit approval |
| GitHub Actions workflow file | High | intense + explicit approval |

---

## Pre-Edit Checklist — `strict` Mode

Before touching the file:

- [ ] Read the target file
- [ ] Searched for existing helper/pattern that does this
- [ ] Checked requirements.txt for any dep being used
- [ ] Estimated blast radius: how many other files import from here?
- [ ] Chose one verification method (existing test / manual curl / new regression test)

---

## Pre-Edit Checklist — `intense` Mode

Before touching the file:

- [ ] Read the target file in full
- [ ] Read all files that import from the target (check callers)
- [ ] Searched for existing helper/pattern
- [ ] Opened requirements.txt / pyproject.toml — confirmed every dep being used is listed
- [ ] No new dep unless user explicitly approves this turn
- [ ] Identified security / validation / data-integrity risks
- [ ] Written a minimal patch plan in 3 sentences or fewer
- [ ] Chosen rollback-neutral approach (no data loss if reverted)
- [ ] Chosen verification: test command or specific manual check
- [ ] For NVIDIA API changes: confirmed key is read via os.getenv(), never hardcoded

---

## Verification Quick Reference

| Change | Minimum Verification |
|---|---|
| New route | `pytest tests/test_<module>.py -v` or manual `curl` with expected response |
| Schema change | `pytest` for affected endpoints; check 422 behavior with invalid input |
| CRUD change | `pytest tests/` for CRUD tests; check both success and constraint-violation |
| NVIDIA API change | Mock test confirming env var is read; curl against a safe sandbox endpoint |
| Auth change | Negative test: unauthenticated request must be rejected |
| Migration | `alembic upgrade head` in dev; confirm rollback with `alembic downgrade -1` |
| Refactor | Existing tests pass; `git diff --stat` shows no new files |

---

## Output Template (copy this every time)

```
Changed:
- <path/to/file.py> — <what changed in one line>

Verified:
- <command run or manual check performed>

Skipped:
- <what was intentionally not done>

Add when:
- <specific condition that justifies adding the skipped work>

Approval needed:
- <only if a high-risk action is pending>
```
