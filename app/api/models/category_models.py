import uuid
from api.models.base_api_model import BaseApiModel


class CategoryBase(BaseApiModel):
    name: str
    description: str

class CategoryGet(CategoryBase):
    id: uuid.UUID
