from fastapi import FastAPI

from config.logging import configure_logging
from presentation.routes.auth import router as auth_router
from presentation.routes.workouts import router as workouts_router
from presentation.routes.meals import router as meals_router
from presentation.routes.water import router as water_router
from presentation.routes.dashboard import router as dashboard_router
from presentation.routes.ai import router as ai_router


configure_logging()

app = FastAPI(title="Health Monitor API", version="0.1.0")


@app.get("/health", tags=["health"])
def health() -> dict:
    return {"status": "ok"}


app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(workouts_router, prefix="/api/workouts", tags=["workouts"])
app.include_router(meals_router, prefix="/api/meals", tags=["meals"])
app.include_router(water_router, prefix="/api/water", tags=["water"])
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(ai_router, prefix="/api/ai", tags=["ai"])

