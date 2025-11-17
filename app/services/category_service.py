
from typing import Annotated, List
from uuid import UUID
from fastapi import Depends, Response, status
from api.models.category_models import CategoryGet, CategoryCreate, CategoryUpdate
from api.models.auth_models import UserGet
from db.entities.user_entities import User
from db.entities.types.category_type import CategoryType
from db.entities.category_entities import Category
from db.dao.category_dao import CategoryDao, CategoryDaoInstance


class CategoryService:
    def __init__(self, dao: CategoryDao):
        self.dao = dao

    async def get_predefined_categories(self) -> List[CategoryGet]:
        categories = await self.dao.get_predefined_categories()
        return [CategoryGet.model_validate(category) for category in categories]
    
    async def get_predefined_expense_categories(self) -> List[CategoryGet]:
        categories = await self.dao.get_predefined_categories(CategoryType.EXPENSE)
        return [CategoryGet.model_validate(category) for category in categories]
    
    async def get_predefined_income_categories(self) -> List[CategoryGet]:
        categories = await self.dao.get_predefined_categories(CategoryType.INCOME)
        return [CategoryGet.model_validate(category) for category in categories]
    
    async def get_categories(self, current_user: UserGet) -> List[CategoryGet]:
        categories = await self.dao.get_categories(current_user.id)
        return [CategoryGet.model_validate(category) for category in categories]
    
    async def get_expense_categories(self, current_user: UserGet) -> List[CategoryGet]:
        categories = await self.dao.get_categories(current_user.id, CategoryType.EXPENSE)
        return [CategoryGet.model_validate(category) for category in categories]
    
    async def get_income_categories(self, current_user: UserGet) -> List[CategoryGet]:
        categories = await self.dao.get_categories(current_user.id, CategoryType.INCOME)
        return [CategoryGet.model_validate(category) for category in categories]
    
    async def get_user_custom_expense_categories(self, current_user: User):
        expense_categories = [
            category for category in current_user.categories 
            if category.category_type == CategoryType.EXPENSE.value
        ]
        return [CategoryGet.model_validate(category) for category in expense_categories]
    
    async def get_user_custom_income_categories(self, current_user: User):
        income_categories = [
            category for category in current_user.categories 
            if category.category_type == CategoryType.INCOME.value
        ]
        return [CategoryGet.model_validate(category) for category in income_categories]
    
    async def get_category_by_id(self, category_id: UUID) -> CategoryGet:
        category = await self.dao.get_by_id(Category, category_id)
        return CategoryGet.model_validate(category)
    
    async def create_new_category(self, current_user: UserGet, request: CategoryCreate) -> CategoryGet:
        request.user_id = current_user.id
        request.is_predefined = False
        category = await self.dao.create(Category, **request.model_dump())
        return CategoryGet.model_validate(category)
    
    async def update_category(self, category_id: UUID, request: CategoryUpdate) -> CategoryGet:
        category_updated = await self.dao.update(Category, category_id, request)
        return CategoryGet.model_validate(category_updated)

    async def delete_category(self, category_id: UUID):
        await self.dao.delete_by_id(Category, category_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    async def delete_category_permanently(self, category_id: UUID):
        await self.dao.delete_by_id(Category, category_id, True)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

def get_category_service(dao: CategoryDaoInstance) -> CategoryService:
    return CategoryService(dao)


CategoryServiceInstance = Annotated[CategoryService, Depends(get_category_service)]
