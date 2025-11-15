from typing import Optional
import uuid
from pydantic import ConfigDict
from api.models.base_api_model import BaseApiModel


class CategoryBase(BaseApiModel):
    name: str
    description: str

class CategoryGet(CategoryBase):
    id: uuid.UUID

class CategoryRequest(CategoryBase):
    user_id: Optional[uuid.UUID] = None
    is_predefined: bool = False

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Savings",
                    "description": "Emergency fund and investments"
                }
            ]
        }
    )
