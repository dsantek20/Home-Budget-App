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

class IncomeUpdate(IncomeBase):
    amount: Optional[Decimal] =  Field(None, gt=0, description="Income amount (must be positive)")
    description: Optional[str] = None
    income_date: Optional[date] = None
    category_id: Optional[uuid.UUID] = None

class IncomeFilter(BaseApiModel):
    category_id: Optional[uuid.UUID] = None
    min_amount: Optional[Decimal] = Field(None, ge=0)
    max_amount: Optional[Decimal] = Field(None, ge=0)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = None
    limit: Optional[int] = Field(None, ge=1) 
