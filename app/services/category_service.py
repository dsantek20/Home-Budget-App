
from typing import Annotated, List
from uuid import UUID
from fastapi import Depends
from api.models.category_models import CategoryGet, CategoryRequest, CategoryUpdate
from api.models.auth_models import UserGet
from db.entities.category_entities import Category
from db.dao.category_dao import CategoryDao, CategoryDaoInstance


class CategoryService:
    def __init__(self, dao: CategoryDao):
        self.dao = dao

    async def get_predefined_categories(self) -> List[CategoryGet]:
        categories = await self.dao.get_predefined_categories()
        return [CategoryGet.model_validate(category) for category in categories]
    
    async def get_categories(self, current_user: UserGet) -> List[CategoryGet]:
        categories = await self.dao.get_categories(current_user.id)
        return [CategoryGet.model_validate(category) for category in categories]
    
    async def get_category_by_id(self, category_id: UUID) -> CategoryGet:
        category = await self.dao.get_by_id(Category, category_id)
        return CategoryGet.model_validate(category)
    
    async def create_new_category(self, current_user: UserGet, request: CategoryRequest) -> CategoryGet:
        request.user_id = current_user.id
        request.is_predefined = False
        category = await self.dao.create(Category, **request.model_dump())
        return CategoryGet.model_validate(category)
    
    async def update_category(self, category_id: UUID, request: CategoryUpdate) -> CategoryGet:
        category_updated = await self.dao.update(Category, category_id, request)
        return CategoryGet.model_validate(category_updated)


def get_category_service(dao: CategoryDaoInstance) -> CategoryService:
    return CategoryService(dao)


CategoryServiceInstance = Annotated[CategoryService, Depends(get_category_service)]
