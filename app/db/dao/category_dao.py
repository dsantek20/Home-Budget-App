from typing import Annotated, List, Optional
from fastapi import Depends
from sqlalchemy import and_, or_, select
from db.entities.types.category_type import CategoryType
from db.entities.category_entities import Category
from db.dao.base_dao import BaseDAO
from db.database import DatabaseSession


class CategoryDao(BaseDAO):
    
    async def get_predefined_categories(self, category_type: Optional[CategoryType] = None) -> List[Category]:
        query = select(Category).where(Category.is_predefined == True, Category.deleted_at.is_(None))
        if category_type:
            query = query.where(Category.category_type == category_type.value)
        result = await self.run_query(query=query)
        return result.scalars().all()
    
    async def get_categories(self, user_id, category_type: Optional[CategoryType] = None) -> List[Category]:
        query = select(Category).where(
            and_(
                Category.deleted_at.is_(None), 
                or_(
                    Category.is_predefined == True,
                    Category.user_id == user_id
                )
            )
        )

        if category_type:
            query = query.where(Category.category_type == category_type.value)
        
        result = await self.run_query(query=query)
        return result.scalars().all()

def get_category_dao(session: DatabaseSession) -> CategoryDao:
    return CategoryDao(session)


CategoryDaoInstance = Annotated[CategoryDao, Depends(get_category_dao)]