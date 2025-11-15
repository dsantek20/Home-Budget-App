
from typing import Annotated
from fastapi import Depends, status
from pwdlib import PasswordHash
from api.models.auth_models import UserCreate, UserGet, UserLoginGet, UserLoginRequest
from auth.users_auth import create_jwt_token
from error_handling.error_handling import ApplicationException
from db.entities.user_entities import User
from db.dao.user_dao import UserDao, UserDaoInstance


class AuthService:
    def __init__(self, dao: UserDao):
        self.dao = dao

    def get_password_hash(self, password):
        return PasswordHash.recommended().hash(password)
    
    def verify_password(self, plain_password, hashed_password):
        return PasswordHash.recommended().verify(plain_password, hashed_password)

    async def register_user(self, request: UserCreate):
        request.password = self.get_password_hash(request.password)
        user = await self.dao.create(User, **request.model_dump())
        return UserGet.model_validate(user)
    
    async def login_user(self, request: UserLoginRequest) -> UserLoginGet:
        user = await self.dao.get_by_email(request.email)
        if not user or not self.verify_password(request.password, user.password):
            raise ApplicationException(status_code=status.HTTP_401_UNAUTHORIZED, code="SVC-4000", message="Invalid username or password", debug_message="User not found or password mismatch")
        user_response = UserLoginGet.model_validate(user)
        user_response.access_token = create_jwt_token(user.email)
        return user_response


def get_auth_service(dao: UserDaoInstance) -> AuthService:
    return AuthService(dao)


AuthServiceInstance = Annotated[AuthService, Depends(get_auth_service)]
