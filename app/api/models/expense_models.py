from datetime import datetime
from decimal import Decimal
from typing import Optional
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

class ExpenseUpdate(ExpenseBase):
    amount: Optional[Decimal] = Field(None, gt=0, description="Cost amount (must be positive)")
    description: Optional[str] = None
    expense_date: Optional[datetime] = None
    category_id: Optional[uuid.UUID] = None