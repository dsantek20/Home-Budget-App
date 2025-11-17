from datetime import date
from decimal import Decimal
from typing import Optional
import uuid
from pydantic import Field
from api.models.base_api_model import BaseApiModel
from api.models.category_models import CategoryGet


class IncomeBase(BaseApiModel):
    amount: Decimal = Field(..., gt=0, description="Income amount (must be positive)")
    description: str
    income_date: date

class IncomeGet(IncomeBase):
    id: uuid.UUID
    category: CategoryGet

class IncomeCreate(IncomeBase):
    category_id: uuid.UUID
