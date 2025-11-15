
from typing import Annotated, List
from fastapi import Depends
from api.models.category_models import CategoryGet
from db.dao.category_dao import CategoryDao, CategoryDaoInstance


class CategoryService:
    def __init__(self, dao: CategoryDao):
        self.dao = dao

    async def get_predefined_categories(self) -> List[CategoryGet]:
        categories = await self.dao.get_predefined_categories()
        return [CategoryGet.model_validate(category) for category in categories]


def get_category_service(dao: CategoryDaoInstance) -> CategoryService:
    return CategoryService(dao)


CategoryServiceInstance = Annotated[CategoryService, Depends(get_category_service)]
