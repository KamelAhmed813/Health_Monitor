from __future__ import annotations

from fastapi import APIRouter

from app.use_cases.auth_login import auth_login
from app.use_cases.auth_register import auth_register
from presentation.dependencies import get_user_repo
from presentation.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from presentation.security.jwt import create_access_token, hash_password


router = APIRouter()


@router.post("/register", response_model=TokenResponse)
def register(request: RegisterRequest) -> TokenResponse:
    user_repo = get_user_repo()
    password_hash = hash_password(request.password)
    user = auth_register(email=request.email, password_hash=password_hash, user_repo=user_repo)

    return TokenResponse(access_token=create_access_token(subject=user.id), token_type="bearer")


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest) -> TokenResponse:
    user_repo = get_user_repo()
    token = auth_login(email=request.email, password=request.password, user_repo=user_repo)
    return TokenResponse(access_token=token, token_type="bearer")

