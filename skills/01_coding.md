# Coding Standards

These rules apply globally to all code generated in any opencode session.
Project-level `.opencode/rules/rules.md` overrides these where they conflict.

---

## Language & Stack

- **Python 3.11+** — type hints on ALL function signatures, no exceptions
- **FastAPI** for APIs; async routes everywhere
- **SQLAlchemy 2.x async** for ORM (`async with session` pattern)
- **pytest + httpx.AsyncClient** for all tests (unit → integration → E2E)
- **Pydantic v2** for request/response models; no raw dicts in API schemas

## Secrets & Config

```python
# ✅ correct
import os
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise RuntimeError("DATABASE_URL not set")

# ❌ never
DB_URL = "postgresql://user:pass@localhost/mydb"
```

- No hardcoded secrets, URLs, or credentials anywhere
- `.env` for local dev; always listed in `.gitignore`
- Validate required env vars at startup, fail fast with a clear message

## Error Handling

```python
# ✅ correct
try:
    result = await some_service.call()
except httpx.TimeoutException as exc:
    logger.error("service timeout: %s", exc)
    raise HTTPException(status_code=504, detail="upstream timeout")

# ❌ never
try:
    result = await some_service.call()
except:
    pass
```

- No bare `except:` — always name the exception
- All FastAPI routes return consistent JSON:
  - Success: `{"status": "ok", "data": {...}}`
  - Error: `{"status": "error", "message": "...", "code": "SNAKE_CASE_CODE"}`

## Code Style

- `logging` over `print()` in all production code
- Path comment header on every generated file: `# path/to/file.py`
- Docstrings on all public functions and classes (Google style)
- `async/await` everywhere in FastAPI — no sync blocking calls
- `requirements.txt` (not `pyproject.toml`) unless project already uses it

## Required Endpoints

Every FastAPI app must have:
```python
@app.get("/health")
async def health():
    return {"status": "ok"}
```

## File Output Format

When generating code files:
- Raw code only — no markdown fences wrapping the output
- Include the file path as a comment on line 1
- Group imports: stdlib → third-party → local (blank line between groups)
