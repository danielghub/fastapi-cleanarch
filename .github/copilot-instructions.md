# Copilot / AI Agent Instructions for this repo

Purpose: Help AI coding agents be immediately productive in this FastAPI project.

Quick summary
- This is a small Clean-architecture FastAPI app. The runtime app is created in `app/main.py` and routers are mounted there.
- Layers: `routers` -> `services` -> `models` (Pydantic) & `models` (SQLAlchemy entities) -> `core` (DB engine/session).

Key files and patterns
- DB setup: `app/core/database.py` defines `engine`, `SessionLocal`, and `Base`. The default DATABASE_URL comes from the env var `DATABASE_URL`.
- DB session injection: `app/core/db_session.py` provides `get_db()` which yields a `SessionLocal()` and is intended to be used with `Depends(get_db)` in routers.
- Router pattern: See `app/routers/user_router.py` — routers accept a Pydantic model (`app/models/user_model.py`) and obtain `db: Session = Depends(get_db)` and service instances via a factory in `app/services/dependencies.py`.
- Services: `app/services/user_service.py` shows the common CRUD pattern: create an SQLAlchemy entity, `db.add()`, `db.commit()`, `db.refresh()`, and return a plain dict. Prefer explicit commit/refresh as in that file.
- Models: Keep a separation between Pydantic input models (`app/models/user_model.py`) and SQLAlchemy entities (`app/models/user_entity.py`). Follow the same naming and mapping style.

Runtime / developer workflows (concrete)
- Install deps: `pip install -r requirements.txt` (project uses SQLAlchemy 2.x, FastAPI, uvicorn, and psycopg2-binary)
- DB: default `DATABASE_URL` is `postgresql://localhost/fastapi_db` (set via env var). For quick local tests you can set `DATABASE_URL` to a sqlite URL if desired.
- Run app locally: `uvicorn app.main:app --reload` from the repository root.
- DB migrations: none present. `app/main.py` calls `Base.metadata.create_all(bind=engine)` at startup — new entities will be created automatically when the app starts.

Coding conventions & expectations for patches
- Small, focused edits: keep changes limited to the relevant layer (router vs service vs model). When adding DB logic, update both the Pydantic model and the SQLAlchemy entity if fields are persisted.
- Dependency injection: use the existing `get_db()` and service factory `get_user_service()` patterns rather than creating ad-hoc singletons.
- Return types: service methods typically return plain serializable Python dicts (not Pydantic models). Follow the simple mapping in `user_service.py` unless adding explicit response models to the router.

Examples to copy from
- Creating a user (router + service flow): see `app/routers/user_router.py` and `app/services/user_service.py` for the exact parameter list and DB usage.
- DB session usage: use `get_db()` from `app/core/db_session.py` and annotate as `db: Session = Depends(get_db)`.

Tests & CI
- There are no tests or CI config in the repo. If you add tests, follow the same layering: call services with a test `Session` (or mock DB) and keep router tests focused on request/response behavior.

When unsure — small checklist
1. Which layer to change? Prefer `services` for business logic, `routers` only for API wiring.
2. Does the change touch persistence? Update the SQLAlchemy `UserEntity` and ensure `Base.metadata.create_all` will handle schema changes locally (or add migrations if necessary).
3. Use `get_db()` and service factories for dependency injection.

If you need more context or want a stricter contributor guide, ask for: preferred test framework, migration tool (alembic), and CI platform.

---
Generated/updated by an AI assistant. Please review and tell me what to clarify or expand.
