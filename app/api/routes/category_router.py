from typing import List
from fastapi import APIRouter, Depends
from uuid import UUID
from api.models.category_models import CategoryGet, CategoryRequest, CategoryUpdate
from services.category_service import CategoryServiceInstance
from auth.dependencies import CurrentUser, get_current_user


category_router = APIRouter(dependencies=[Depends(get_current_user)])


@category_router.get("/predefined", response_model=List[CategoryGet])
async def get_predefined_categories(service: CategoryServiceInstance):
    return await service.get_predefined_categories()

@category_router.get("/custom", response_model=List[CategoryGet])
async def get_user_custom_categories(current_user: CurrentUser):
    return [CategoryGet.model_validate(category) for category in current_user.categories]

@category_router.get("/", response_model=List[CategoryGet])
async def get_categories(current_user: CurrentUser, service: CategoryServiceInstance):
    return await service.get_categories(current_user)

@category_router.get("/{category_id}", response_model=CategoryGet)
async def get_category_by_id(category_id: UUID, service: CategoryServiceInstance):
    return await service.get_category_by_id(category_id)

@category_router.post("/", response_model=CategoryGet)
async def create_new_category(current_user: CurrentUser, request: CategoryRequest, service: CategoryServiceInstance):
    return await service.create_new_category(current_user, request)

@category_router.patch("/{category_id}", response_model=CategoryGet)
async def update_category(category_id: UUID, request: CategoryUpdate, service: CategoryServiceInstance):
    return await service.update_category(category_id, request)

@category_router.delete("/{category_id}")
async def delete_category(category_id: UUID, service: CategoryServiceInstance):
    return await service.delete_category(category_id)