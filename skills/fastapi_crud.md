# Skill: FastAPI CRUD with SQLAlchemy Async

**When to use this skill:**
User asks to create a REST API, a CRUD endpoint set, a database model,
or anything involving FastAPI + a relational database.

---

## Canonical File Structure

```
<project>/
├── app/
│   ├── main.py          # FastAPI app factory
│   ├── models.py        # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic v2 request/response schemas
│   ├── crud.py          # DB operations (no business logic)
│   ├── routers/
│   │   └── <resource>.py
│   └── database.py      # engine + session factory
├── tests/
│   ├── conftest.py      # async test client + test DB
│   └── test_<resource>.py
└── requirements.txt
```

---

## database.py — Template

```python
# app/database.py
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
import os

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
```

---

## models.py — Template

```python
# app/models.py
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
import uuid


class Item(Base):
    __tablename__ = "items"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
```

---

## schemas.py — Template

```python
# app/schemas.py
from pydantic import BaseModel
from datetime import datetime


class ItemCreate(BaseModel):
    name: str


class ItemResponse(BaseModel):
    id: str
    name: str
    created_at: datetime

    model_config = {"from_attributes": True}
```

---

## crud.py — Template

```python
# app/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import Item
from .schemas import ItemCreate


async def create_item(db: AsyncSession, data: ItemCreate) -> Item:
    item = Item(name=data.name)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def get_item(db: AsyncSession, item_id: str) -> Item | None:
    result = await db.execute(select(Item).where(Item.id == item_id))
    return result.scalar_one_or_none()


async def list_items(db: AsyncSession) -> list[Item]:
    result = await db.execute(select(Item))
    return list(result.scalars().all())
```

---

## Router — Template

```python
# app/routers/items.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import ItemCreate, ItemResponse
from .. import crud

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=ItemResponse, status_code=201)
async def create(payload: ItemCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_item(db, payload)


@router.get("/{item_id}", response_model=ItemResponse)
async def read(item_id: str, db: AsyncSession = Depends(get_db)):
    item = await crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/", response_model=list[ItemResponse])
async def list_all(db: AsyncSession = Depends(get_db)):
    return await crud.list_items(db)
```

---

## Test Fixture — conftest.py

```python
# tests/conftest.py
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.main import app
from app.database import Base, get_db

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(TEST_DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session
    await engine.dispose()

@pytest_asyncio.fixture
async def client(db_session):
    async def override_db():
        yield db_session
    app.dependency_overrides[get_db] = override_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
    app.dependency_overrides.clear()
```

---

## Checklist Before Delivering

- [ ] `GET /health` returns `{"status": "ok"}`
- [ ] No hardcoded DB URL — reads from `os.getenv("DATABASE_URL")`
- [ ] All routes have Pydantic response models
- [ ] At least one happy-path test per endpoint
- [ ] `requirements.txt` includes: fastapi, uvicorn, sqlalchemy, asyncpg (or aiosqlite for tests), pydantic, httpx, pytest-asyncio
