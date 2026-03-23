# Health Monitor Backend

FastAPI + Redis + SQLite + Google GenAI monolith skeleton.

## Local development

1. Create a virtualenv and install deps:
   - `pip install -r requirements.txt`
2. Run the API:
   - `uvicorn main:app --reload --port 8000`

## Configuration

Environment variables are read via `backend/config/settings.py`.

Recommended:
- `HEALTH_JWT_SECRET`
- `HEALTH_REDIS_URL`
- `HEALTH_SQLITE_PATH`
- `HEALTH_GOOGLE_GENAI_API_KEY`
