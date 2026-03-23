from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from presentation.security.jwt import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = decode_access_token(token)
        sub = payload.get("sub")
        if sub is None:
            raise ValueError("Missing sub claim")
        return int(sub)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        ) from e


def get_user_repo():
    # Lazy import to keep skeleton imports robust.
    from infrastructure.db.repositories.user_repo_impl import UserRepositoryImpl
    from infrastructure.db.session import get_session

    session = get_session()
    return UserRepositoryImpl(session)


def get_workout_repo():
    from infrastructure.db.repositories.workout_repo_impl import WorkoutRepositoryImpl
    from infrastructure.db.session import get_session

    session = get_session()
    return WorkoutRepositoryImpl(session)


def get_meal_repo():
    from infrastructure.db.repositories.meal_repo_impl import MealRepositoryImpl
    from infrastructure.db.session import get_session

    session = get_session()
    return MealRepositoryImpl(session)


def get_water_repo():
    from infrastructure.db.repositories.water_repo_impl import WaterRepositoryImpl
    from infrastructure.db.session import get_session

    session = get_session()
    return WaterRepositoryImpl(session)


def get_target_repo():
    from infrastructure.db.repositories.target_repo_impl import TargetRepositoryImpl
    from infrastructure.db.session import get_session

    session = get_session()
    return TargetRepositoryImpl(session)


def get_cache():
    from infrastructure.cache.redis_cache import RedisCacheService
    from config.settings import settings

    return RedisCacheService(redis_url=settings.redis_url)


def get_ai_service():
    from infrastructure.ai.genai_service import GenAiService
    from config.settings import settings

    return GenAiService(api_key=settings.google_genai_api_key)

