# LessWorks Patterns — Python / FastAPI / NVIDIA Stack

Minimal, correct patterns for the actual stack in use.
Each pattern is the smallest safe implementation — use it verbatim or adapt minimally.

---

## 1. Route Patterns

### Minimal GET route (read one record)
```python
# app/routes/<resource>.py
@router.get("/{item_id}", response_model=schemas.ItemRead)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```
**What to skip:** custom error class, logging decorator, middleware wrapper — unless already in the project.

### Minimal POST route (create)
```python
@router.post("/", response_model=schemas.ItemRead, status_code=201)
async def create_item(payload: schemas.ItemCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_item(db, payload)
```
**What to skip:** transaction wrapper (SQLAlchemy async session handles it), separate validation layer (Pydantic handles it).

### Minimal /health endpoint
```python
# app/main.py or app/routes/health.py
@app.get("/health")
async def health():
    return {"status": "ok"}
```
**Nothing else needed** unless the project already checks DB connectivity — add that only when the health check is used by a load balancer that needs DB state.

---

## 2. Schema Patterns

### Minimal Pydantic schema set
```python
# app/schemas.py
from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass  # add fields only if creation needs extras not in Base

class ItemRead(ItemBase):
    id: int
    model_config = {"from_attributes": True}
```
**What to skip:** `ItemUpdate` schema — add only when the project has a PATCH route. Avoid creating all schemas upfront.

### Adding a field to an existing schema
```python
# Minimal diff — add only the new field
class ItemBase(BaseModel):
    name: str
    description: str | None = None
    status: str = "active"  # ← only this line added
```
**What to skip:** touching unrelated fields, renaming anything, restructuring the schema.

---

## 3. CRUD Patterns

### Minimal async CRUD function
```python
# app/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models, schemas

async def get_item(db: AsyncSession, item_id: int) -> models.Item | None:
    result = await db.execute(select(models.Item).where(models.Item.id == item_id))
    return result.scalar_one_or_none()

async def create_item(db: AsyncSession, payload: schemas.ItemCreate) -> models.Item:
    item = models.Item(**payload.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item
```
**What to skip:** repository pattern, base CRUD class, generic type parameters — add only when 3+ models share identical CRUD logic.

---

## 4. NVIDIA API Patterns

### Minimal async NVIDIA call (httpx — already installed with FastAPI)
```python
# app/services/nvidia.py
import os
import httpx
import logging

logger = logging.getLogger(__name__)

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

async def call_nvidia_model(model: str, prompt: str) -> str:
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("NVIDIA_API_KEY not set")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{NVIDIA_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1024,
            },
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
```
**Security rules (non-negotiable):**
- Key ALWAYS via `os.getenv()` — never hardcoded, never logged
- Never include the key in error messages, stack traces, or response bodies
- Always set a `timeout` — never leave it as `None` for an external API

### Minimal streaming NVIDIA call
```python
async def stream_nvidia_model(model: str, prompt: str):
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("NVIDIA_API_KEY not set")

    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            f"{NVIDIA_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": True,
            },
            timeout=60.0,
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: ") and line != "data: [DONE]":
                    yield line[6:]  # strip "data: " prefix
```
**What to skip:** custom SSE parser, retry decorator, circuit breaker — add only if the project shows persistent timeout failures and a retry decision is made explicitly.

### Model reference (nvidia-custom provider)
```python
NVIDIA_MODELS = {
    "reason":   "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",  # math, finance, deterministic
    "code":     "nvidia/nemotron-3-ultra-550b-a55b",               # complex reasoning, code gen
    "fast":     "nvidia/nemotron-3.5-lightning-30b-a3b",           # lightweight, low-latency
    "creative": "meta/muse-glimmer-30b",                           # writing, social, email
    "ads":      "google/gemma-4-31b-it",                           # structured output, campaigns
    "support":  "z-ai/glm-5.3",                                    # classification, support
}
```

---

## 5. Standard Library First — Python Quick Reference

| Task | Use This | Not This |
|---|---|---|
| Generate UUID | `import uuid; uuid.uuid4()` | shortuuid, nanoid, ulid |
| File paths | `from pathlib import Path` | os.path.join() |
| JSON | `import json` | simplejson, orjson (unless installed) |
| Dates | `from datetime import datetime, UTC` | arrow, pendulum (unless installed) |
| Logging | `import logging; logger = logging.getLogger(__name__)` | loguru, structlog (unless installed) |
| Env vars | `import os; os.getenv("VAR", "default")` | python-decouple, dynaconf (unless installed) |
| Async | `import asyncio` | trio, anyio (unless installed) |
| Type hints | `list[str]`, `dict[str, int]`, `str \| None` (Python 3.10+) | `List`, `Dict`, `Optional` from typing |
| HTTP client | `httpx.AsyncClient` (already in FastAPI projects) | requests, aiohttp |

---

## 6. Test Patterns

### Minimal async test (FastAPI + httpx)
```python
# tests/test_<resource>.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

async def test_get_item_happy_path(client):
    response = await client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

async def test_get_item_not_found(client):
    response = await client.get("/items/99999")
    assert response.status_code == 404

async def test_create_item_invalid_payload(client):
    response = await client.post("/items/", json={})  # missing required field
    assert response.status_code == 422
```
**What to skip:** fixtures that mock every dependency upfront, test helpers that mirror the production code, parametrize blocks for every field permutation — add only when a specific edge case bites.

### Minimal NVIDIA API mock
```python
import pytest
from unittest.mock import AsyncMock, patch

async def test_nvidia_call_uses_env_key():
    with patch("app.services.nvidia.httpx.AsyncClient") as mock_client:
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "test response"}}]
        }
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )
        result = await call_nvidia_model("nvidia/nemotron-3-ultra-550b-a55b", "hello")
        assert result == "test response"
```

---

## 7. Logging — Minimum Viable Pattern

```python
import logging

logger = logging.getLogger(__name__)

# In a route or service:
logger.info("Processing request for item_id=%s", item_id)
logger.warning("Item not found: id=%s", item_id)
logger.error("NVIDIA API error: %s", exc, exc_info=True)

# NEVER log:
logger.info("API key: %s", api_key)         # ← security violation
logger.info("Request headers: %s", headers) # ← may contain auth tokens
```

---

## 8. Environment & Secrets Pattern

```python
# app/config.py — only create this file if 3+ settings need grouping
import os
from dataclasses import dataclass

@dataclass
class Settings:
    nvidia_api_key: str = os.getenv("NVIDIA_API_KEY", "")
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./dev.db")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()
```
**What to skip:** pydantic-settings, python-dotenv, dynaconf — use only if the project already has one of these. A plain `os.getenv()` call in the service module is sufficient for 1–2 settings.
