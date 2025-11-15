from typing import Annotated, List, Optional
from fastapi import Depends
from sqlalchemy import select
from db.entities.category_entities import Category
from db.dao.base_dao import BaseDAO
from db.database import DatabaseSession


class CategoryDao(BaseDAO):
    
    async def get_predefined_categories(self) -> List[Category]:
        query = select(Category).where(Category.is_predefined == True, Category.deleted_at.is_(None))
        result = await self.run_query(query=query)
        return result.scalars().all()

def get_category_dao(session: DatabaseSession) -> CategoryDao:
    return CategoryDao(session)


CategoryDaoInstance = Annotated[CategoryDao, Depends(get_category_dao)]