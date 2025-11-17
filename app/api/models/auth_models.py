from decimal import Decimal
from typing import Optional
import uuid
from pydantic import EmailStr
from api.models.base_api_model import BaseApiModel


class UserBase(BaseApiModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    balance: Decimal

class UserGet(UserBase):
    id: uuid.UUID

class UserCreate(UserBase):
    password: str

class UserLoginGet(UserBase):
    id: uuid.UUID
    access_token: Optional[str] = None

class UserLoginRequest(BaseApiModel):
    email: EmailStr
    password: str
