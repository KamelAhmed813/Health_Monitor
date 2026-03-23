# Health Monitor - Project Architecture Map

This document is the canonical reference for any agent working on this repository.
Use it before implementing edits, enhancements, or new features.

## Environment and startup prerequisites

- The project depends on a virtual environment named `monitor` under `./venv`.
- You must activate it before running the app, tests, or installs.

Windows PowerShell:

```powershell
.\venv\monitor\Scripts\Activate.ps1
```

If you are working from the backend folder layout:

```powershell
cd .\backend
.\venv\monitor\Scripts\Activate.ps1
```

Then run:

```powershell
uvicorn main:app --reload --port 8000
```

## High-level architecture

This backend follows a layered/clean architecture style:

1. `presentation` (FastAPI routes + request/response schemas + auth dependency wiring)
2. `app` (use-case orchestration and business application flows)
3. `domain` (core entities and interface contracts/ports)
4. `infrastructure` (DB models, repository implementations, cache, AI adapter, prompt loading)
5. `config` (runtime settings and logging)

Primary request flow:

`HTTP route -> dependency provider -> app use-case -> domain port -> infrastructure implementation -> SQLite/Redis/AI -> response schema`

## File structure map

Top-level:

- `AGENTS.md` - this reference map
- `backend/` - main API service codebase

Backend structure:

- `backend/main.py` - FastAPI app bootstrap, router registration, startup DB table creation, global app error mapping
- `backend/config/`
  - `settings.py` - environment-driven settings (`HEALTH_*`)
  - `logging.py` - logging setup
- `backend/presentation/`
  - `routes/` - endpoint handlers:
    - `auth.py`
    - `workouts.py`
    - `meals.py`
    - `water.py`
    - `dashboard.py`
    - `ai.py`
  - `schemas/` - Pydantic request/response DTOs used by routes
  - `dependencies.py` - dependency wiring: current user, repositories, cache, AI service
  - `security/jwt.py` - password hashing and JWT encode/decode helpers
- `backend/app/`
  - `use_cases/` - application actions (auth, logging workouts/meals/water, dashboard, AI features)
  - `errors.py` - typed app-level exceptions (`AppError`, `ConflictError`, etc.)
- `backend/domain/`
  - `entities/models.py` - immutable core dataclass models
  - `ports/interfaces.py` - repository/cache/AI protocols used by app layer
- `backend/infrastructure/`
  - `db/models.py` - SQLAlchemy table models
  - `db/session.py` - SQLite engine/session factory
  - `db/repositories/*_repo_impl.py` - protocol implementations with cache invalidation logic
  - `cache/redis_cache.py` - Redis cache service adapter
  - `ai/genai_service.py` - AI service adapter (placeholder responses currently)
  - `prompts/` - text prompt templates and loader utility
- `backend/tests/`
  - `test_api_smoke_flow.py` - end-to-end smoke flow covering auth, activity logs, dashboard and caching behavior
- `backend/requirements.txt` - runtime/test dependencies
- `backend/README.md` - basic local setup notes

## Architectural conventions to preserve

- Keep route handlers thin:
  - Parse/validate I/O via schemas.
  - Delegate behavior to use-case functions.
- Keep use-cases framework-agnostic:
  - Use ports/interfaces from `domain.ports`.
  - Avoid importing FastAPI or SQLAlchemy directly in `app/use_cases`.
- Keep domain model-centric:
  - Domain entities are immutable dataclasses.
  - Business interfaces are typed via `Protocol`.
- Keep infrastructure replaceable:
  - Repositories implement domain ports and convert DB rows <-> domain models.
  - Cache adapter is behind `CacheService` interface.
- Keep settings centralized:
  - Add new config in `config/settings.py` with `HEALTH_` prefix conventions.

## Existing best practices already used

- **Dependency inversion:** app layer depends on ports, not concrete DB/Redis/AI clients.
- **Separation of concerns:** presentation/app/domain/infrastructure responsibilities are clearly split.
- **Typed contracts:** protocol-based repository/cache/AI interfaces.
- **Centralized error mapping:** custom app errors mapped once in `main.py`.
- **Cache invalidation at write points:** repository methods clear list/dashboard cache keys after mutations.
- **JWT + password hashing:** authentication handled consistently in security helpers.
- **Smoke testing critical flow:** full register/login/log/dashboard scenario in tests.
- **Environment-driven configuration:** settings are injected via env vars, not hardcoded logic.

## Data and integration dependencies

- **API framework:** FastAPI
- **Database:** SQLite (path from `HEALTH_SQLITE_PATH`)
- **Cache:** Redis (URL from `HEALTH_REDIS_URL`)
- **Auth:** JWT (`python-jose`) + passlib hashing
- **AI integration:** Google GenAI adapter (`google-generativeai`) currently scaffolded with placeholder outputs

## How to extend safely (agent checklist)

When adding a new feature (example: `sleep` tracking), follow this sequence:

1. Add/extend domain entity and port contract in `domain/`.
2. Add use-case function(s) in `app/use_cases/`.
3. Add infrastructure model/repository implementation in `infrastructure/`.
4. Wire repository/service provider in `presentation/dependencies.py`.
5. Add request/response schema in `presentation/schemas/`.
6. Add route endpoint in `presentation/routes/`.
7. Register route in `main.py`.
8. Add or update tests in `backend/tests/`.
9. Consider cache key strategy + invalidation for reads affected by writes.

## Practical guardrails for future agents

- Do not bypass use-cases by embedding business logic in routes.
- Do not couple `app/use_cases` to infrastructure internals.
- Reuse `get_current_user_id` and existing JWT flow for protected endpoints.
- If adding cache keys, use consistent namespaced keys like existing `cache:<resource>:<user_id>:<date>`.
- Prefer returning explicit response schemas over ad-hoc dicts for stable API evolution.
- Keep placeholder AI adapters behind `AIService` so implementation can be swapped without route changes.

## Known current limitations

- AI service methods return placeholders, not live model calls yet.
- Some endpoints still return minimal skeleton payloads (e.g., meal/water creation IDs only).
- DB sessions are created in simple helper style; lifecycle can be improved with request-scoped dependency management later.

