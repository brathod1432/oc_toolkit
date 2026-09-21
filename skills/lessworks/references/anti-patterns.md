# LessWorks Anti-Patterns — What Over-Engineering Looks Like Here

These are the most common ways code gets bloated in Python/FastAPI/NVIDIA projects.
Each entry states the bloat, why it's a problem, and the minimal alternative.

---

## 1. Abstraction Anti-Patterns

### ❌ Generic Base CRUD Class (too early)
```python
# Over-engineered: created when there's only one model
class BaseCRUD(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
    async def get(self, db, id): ...
    async def create(self, db, obj_in): ...
```
**Problem:** Generic classes for a single model add ~50 lines and a `typing.Generic` import, but save zero code when only one model exists.
**Minimal alternative:** Direct async functions in `crud.py`. Add the base class only when model #3 lands and the duplication is provable.

### ❌ Repository Pattern on top of SQLAlchemy
```python
# Over-engineered: SQLAlchemy is already a repository
class UserRepository:
    def __init__(self, session): self.session = session
    def find_by_id(self, id): ...
    def save(self, entity): ...
```
**Problem:** Wraps a perfectly good ORM in an extra layer with no added capability.
**Minimal alternative:** `crud.get_user(db, user_id)` directly.

### ❌ Strategy Pattern for a Single Provider
```python
class LLMProvider(ABC):
    @abstractmethod
    async def complete(self, prompt): ...

class NvidiaProvider(LLMProvider):
    async def complete(self, prompt): ...
```
**Problem:** Abstraction for a hypothetical second provider that doesn't exist yet.
**Minimal alternative:** `await call_nvidia_model(model, prompt)` directly. Add the interface when provider #2 is confirmed.

### ❌ Event Bus / Message Queue for In-Process Calls
```python
# Premature: adding Redis pub/sub or Celery for a 3-endpoint MVP
task = celery_app.delay("process_idea", idea_id)
```
**Problem:** Adds infrastructure complexity (Redis, worker process, serialization) before load justifies it.
**Minimal alternative:** Direct `await service_function()` inside the route. Add a queue when the first timeout complaint arrives with data.

---

## 2. Dependency Anti-Patterns

### ❌ Installing libraries the stdlib already handles
```python
# ❌
import shortuuid; shortuuid.uuid()
import arrow; arrow.now()
import loguru; from loguru import logger
import python_dotenv; load_dotenv()
```
```python
# ✅ stdlib equivalents
import uuid; uuid.uuid4()
from datetime import datetime, UTC; datetime.now(UTC)
import logging; logger = logging.getLogger(__name__)
import os; os.getenv("KEY")
```

### ❌ Using a library before checking if it's installed
```python
# ❌ — imports something not in requirements.txt
from pydantic_settings import BaseSettings
```
**Rule:** Check `requirements.txt` or `pyproject.toml` before using any import. If it's not there, it's not available.

### ❌ `requirements.txt` bloat
Adding packages "just in case":
```
celery>=5.3
redis>=5.0
flower>=2.0
sentry-sdk>=1.40
prometheus-fastapi-instrumentator>=6.1
```
**Problem:** Every extra dependency is a supply chain risk, a version conflict surface, and a container size increase.
**Minimal alternative:** Add each only when the specific problem it solves is the current blocker.

---

## 3. File Structure Anti-Patterns

### ❌ Premature module explosion
```
app/
├── interfaces/
│   └── llm_interface.py
├── adapters/
│   └── nvidia_adapter.py
├── domain/
│   └── entities/
│       └── item_entity.py
├── infrastructure/
│   └── repositories/
│       └── item_repository.py
```
**Problem:** Hexagonal/clean architecture for a 3-model MVP adds 8+ empty files and forces every change across 4 directories.
**Minimal alternative:**
```
app/
├── main.py
├── models.py
├── schemas.py
├── crud.py
├── routes/
│   └── items.py
└── services/
    └── nvidia.py
```
Split only when a module grows past ~300 lines or has a clear separation of concern.

### ❌ Creating a new file for every function
```
app/utils/
├── string_utils.py      # has 1 function
├── date_utils.py        # has 1 function
├── response_utils.py    # has 1 function
└── validation_utils.py  # has 1 function
```
**Minimal alternative:** One `app/utils.py` file until it exceeds ~200 lines, then split by actual groupings.

---

## 4. FastAPI-Specific Anti-Patterns

### ❌ Custom exception handler for every HTTP error
```python
# ❌ — FastAPI's HTTPException already handles this
@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": str(exc)})
```
**Minimal alternative:** `raise HTTPException(status_code=404, detail="Item not found")` — unless the project already has a global error handler.

### ❌ Custom dependency for something Depends() already does
```python
# ❌ — wrapper around Depends() adds nothing
def get_current_user_service(db = Depends(get_db)):
    return UserService(db)
```
**Minimal alternative:** Pass `db: AsyncSession = Depends(get_db)` directly to the route and call crud functions inline.

### ❌ Response envelope on every endpoint
```python
# ❌ — wrapping every response in {"status": "ok", "data": {...}}
return {"status": "ok", "data": item, "meta": {"timestamp": ...}}
```
**Problem:** Forces every client to unwrap. FastAPI's `response_model` already structures responses.
**Minimal alternative:** Return the Pydantic model directly. Add an envelope only if the API contract explicitly requires it.

### ❌ Versioning before there's a breaking change
```python
# ❌ — /api/v1/ prefix when there is no v2 planned
@app.include_router(router, prefix="/api/v1/items")
```
**Minimal alternative:** `/items` directly. Add `/v1/` only when a breaking change is imminent and both versions must coexist.

---

## 5. NVIDIA API Anti-Patterns

### ❌ Hardcoded API key
```python
# ❌ — NEVER
API_KEY = "nvapi-..."
headers = {"Authorization": f"Bearer {API_KEY}"}
```

### ❌ Logging the API key
```python
# ❌
logger.debug("Using API key: %s", os.getenv("NVIDIA_API_KEY"))
```

### ❌ No timeout on external HTTP calls
```python
# ❌ — will hang forever on a slow NVIDIA response
async with httpx.AsyncClient() as client:
    response = await client.post(url, ...)
```
**Minimal fix:** `timeout=30.0` for standard calls, `timeout=60.0` for streaming.

### ❌ Building a custom model router before the project uses more than one model
```python
# ❌ premature
class NvidiaModelRouter:
    def __init__(self, strategy: ModelSelectionStrategy): ...
    async def route(self, task_type: str, prompt: str): ...
```
**Minimal alternative:** Pass the model string directly. Add routing logic only when two different models are actively used and the selection logic is tested.

---

## 6. Testing Anti-Patterns

### ❌ Mocking everything upfront
```python
# ❌ — creates a fake version of the whole app before any real test fails
@pytest.fixture
def mock_db(): ...
@pytest.fixture
def mock_nvidia(): ...
@pytest.fixture
def mock_auth(): ...
@pytest.fixture
def mock_cache(): ...
```
**Minimal alternative:** One `AsyncClient` fixture hitting the actual in-memory SQLite test DB. Add mocks only for external services (NVIDIA API) that shouldn't be called in tests.

### ❌ 100% coverage as the target
Writing tests to hit every line, including:
- Getters and setters
- `__repr__` methods
- Config dataclass field accessors

**Minimal alternative:** Test behavior, not lines. A route that creates an item, returns 201, and rejects invalid input is fully tested with 3 assertions.

### ❌ Snapshot testing for API responses
```python
# ❌ — breaks on any formatting change
assert response.json() == snapshot("create_item_response")
```
**Minimal alternative:** Assert only the fields that matter:
```python
data = response.json()
assert data["name"] == payload["name"]
assert "id" in data
assert response.status_code == 201
```

---

## 7. opencode / Agent Anti-Patterns

### ❌ Writing new skill files for every solved problem
If the solution is a 10-line Python function, it does not need a new skill file. Skills are for reusable patterns with context, not individual function implementations.

### ❌ Updating BD_README.md with trivial changes
BD_README.md gets updated after tasks that change architecture, add new modules, or establish new patterns — not after every bugfix or field addition.

### ❌ Creating new BD_tasks/ files for sub-steps
One `bdev-YYYYMMDD-NNN.json` per user request. Internal sub-steps live inside the task's `steps` array, not as separate task files.

### ❌ Running `pip install` without checking requirements.txt first
The agent must read `requirements.txt` before any import or install. If a package is missing, ask for approval before adding it — do not silently install.
