from typing import List
from fastapi import APIRouter, Depends
from api.models.category_models import CategoryGet, CategoryRequest
from services.category_service import CategoryServiceInstance
from auth.dependencies import CurrentUser, get_current_user


category_router = APIRouter(dependencies=[Depends(get_current_user)])


@category_router.get("/predefined", response_model=List[CategoryGet])
async def get_predefined_categories(service: CategoryServiceInstance):
    return await service.get_predefined_categories()

@category_router.post("/create", response_model=CategoryGet)
async def create_new_category(current_user: CurrentUser, request: CategoryRequest, service: CategoryServiceInstance):
    return await service.create_new_category(current_user, request)