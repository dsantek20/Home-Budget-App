from typing import Annotated
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from error_handling.error_handling import ApplicationException
from auth.users_auth import verify_jwt_token
from db.entities.user_entities import User
from db.dao.user_dao import UserDao, get_user_dao


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme), dao: UserDao = Depends(get_user_dao)) -> User:
    try:
        payload = verify_jwt_token(token)
        email: str = payload.get("sub")

    except ApplicationException:
        raise

    user = await dao.get_by_email(email)
    
    if user is None:
        raise ApplicationException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            debug_message="User not found in database",
            message="Invalid credentials",
            code="SVC-4001"
        )
    
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]