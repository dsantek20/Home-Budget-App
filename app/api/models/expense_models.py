from datetime import datetime
from decimal import Decimal
import uuid
from pydantic import Field
from api.models.base_api_model import BaseApiModel
from api.models.category_models import CategoryGet


class ExpenseBase(BaseApiModel):
    amount: Decimal = Field(..., gt=0, description="Cost amount (must be positive)")
    description: str
    expense_date: datetime

class ExpenseGet(ExpenseBase):
    id: uuid.UUID
    category: CategoryGet

class ExpenseCreate(ExpenseBase):
    category_id: uuid.UUID
