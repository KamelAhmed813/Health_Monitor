from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.errors import AppError
from config.logging import configure_logging
from infrastructure.db.models import Base
from infrastructure.db.session import engine
from presentation.routes.auth import router as auth_router
from presentation.routes.workouts import router as workouts_router
from presentation.routes.meals import router as meals_router
from presentation.routes.water import router as water_router
from presentation.routes.dashboard import router as dashboard_router
from presentation.routes.ai import router as ai_router


configure_logging()

app = FastAPI(title="Health Monitor API", version="0.1.0")


@app.exception_handler(AppError)
async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health", tags=["health"])
def health() -> dict:
    return {"status": "ok"}


app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(workouts_router, prefix="/api/workouts", tags=["workouts"])
app.include_router(meals_router, prefix="/api/meals", tags=["meals"])
app.include_router(water_router, prefix="/api/water", tags=["water"])
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(ai_router, prefix="/api/ai", tags=["ai"])

