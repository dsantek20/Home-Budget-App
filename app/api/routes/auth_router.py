from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from api.models.auth_models import UserCreate, UserGet, UserLoginGet, UserLoginRequest
from auth.dependencies import CurrentUser
from services.auth_service import AuthServiceInstance


auth_router = APIRouter()

@auth_router.post("/register", response_model=UserGet, openapi_extra={"security": []})
async def register_user(request: UserCreate, service: AuthServiceInstance):
    return await service.register_user(request)

@auth_router.post("/login", response_model=UserLoginGet, openapi_extra={"security": []})
async def login_user(request: UserLoginRequest, service: AuthServiceInstance):
    return await service.login_user(request)

@auth_router.post("/token", response_model=UserLoginGet)
async def login_for_oauth(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], service: AuthServiceInstance):
    request = UserLoginRequest(email=form_data.username, password=form_data.password)
    return await service.login_user(request)

@auth_router.get("/me", response_model=UserGet)
async def get_me(current_user: CurrentUser):
    return current_user