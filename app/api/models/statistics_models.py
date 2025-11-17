from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional

from pydantic import Field
from api.models.base_api_model import BaseApiModel


class TransactionSummary(BaseApiModel):
    id: str
    amount: float
    description: str
    date: str
  
class CategoryBreakdown(BaseApiModel):
    category: str
    total: float
    count: int
    percentage: float
    average: float
    transactions: List[TransactionSummary]

class ExpenseSummary(BaseApiModel):
    period: str 
    total_spent: float
    expense_count: int 
    average_expense: float 
    categories: List[CategoryBreakdown] 
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class IncomeSummary(BaseApiModel):
    period: str 
    total_income: float
    income_count: int 
    average_income: float 
    categories: List[CategoryBreakdown] 
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class CategoryAggregate(BaseApiModel):
    total: Decimal = Decimal("0")
    count: int = 0
    transactions: List[TransactionSummary] = Field(default_factory=list)

class Categories(BaseApiModel):
    category_name: str
    category_data: CategoryAggregate

class FinancialOverview(BaseApiModel):
    period: str
    total_income: float
    total_expenses: float
    net_balance: float 
    current_account_balance: float 
    start_date: Optional[str] = None
    end_date: Optional[str] = None

