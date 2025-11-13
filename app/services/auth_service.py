
from typing import Annotated
from fastapi import Depends
from pwdlib import PasswordHash
from api.models.auth_models import UserCreate, UserGet
from db.entities.user_entities import User
from db.dao.user_dao import UserDao, UserDaoInstance


class AuthService:
    def __init__(self, dao: UserDao,):
        self.dao = dao

    def get_password_hash(self, password):
        return PasswordHash.recommended().hash(password)

    async def register_user(self, request: UserCreate):
        request.password = self.get_password_hash(request.password)
        user = await self.dao.create(User, **request.model_dump())
        return UserGet.model_validate(user)


def get_auth_service(dao: UserDaoInstance) -> AuthService:
    return AuthService(dao)


AuthServiceInstance = Annotated[AuthService, Depends(get_auth_service)]
