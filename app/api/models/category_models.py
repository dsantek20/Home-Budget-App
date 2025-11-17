from typing import Optional
import uuid
from pydantic import ConfigDict
from api.models.base_api_model import BaseApiModel
from db.entities.types.category_type import CategoryType


class CategoryBase(BaseApiModel):
    name: str
    description: str
    category_type: CategoryType

class CategoryGet(CategoryBase):
    id: uuid.UUID

class CategoryCreate(CategoryBase):
    user_id: Optional[uuid.UUID] = None
    is_predefined: bool = False

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Savings",
                    "description": "Emergency fund and investments",
                    "category_type": "INCOME"
                }
            ]
        }
    )

class CategoryUpdate(BaseApiModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_type: Optional[CategoryType] = None
