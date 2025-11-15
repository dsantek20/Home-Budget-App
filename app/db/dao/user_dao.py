from typing import Annotated, Optional
from fastapi import Depends
from sqlalchemy import select
from db.entities.user_entities import User
from db.dao.base_dao import BaseDAO
from db.database import DatabaseSession


class UserDao(BaseDAO):
    
    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await self.run_query(query=query)
        return result.scalars().first()

def get_user_dao(session: DatabaseSession) -> UserDao:
    return UserDao(session)


UserDaoInstance = Annotated[UserDao, Depends(get_user_dao)]