from fastapi import APIRouter
from api.models.auth_models import UserCreate, UserGet
from services.auth_service import AuthServiceInstance


auth_router = APIRouter()

@auth_router.post("/register", response_model=UserGet, openapi_extra={"security": []})
async def register_user(request: UserCreate, service: AuthServiceInstance):
    return await service.register_user(request)