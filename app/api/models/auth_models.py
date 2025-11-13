import uuid
from pydantic import EmailStr
from api.models.base_api_model import BaseApiModel


class UserBase(BaseApiModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str

class UserGet(UserBase):
    id: uuid.UUID

class UserCreate(UserBase):
    password: str
