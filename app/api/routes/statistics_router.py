from typing import Optional
from fastapi import APIRouter, Depends
from api.models.statistics_models import ExpenseSummary, FinancialOverview, IncomeSummary
from db.entities.types.statistic_type import PeriodType
from auth.dependencies import CurrentUser, get_current_user
from services.statistics_service import StatisticsServiceInstance

statistics_router = APIRouter(dependencies=[Depends(get_current_user)])

@statistics_router.get("/expenses", response_model=ExpenseSummary)
async def get_expense_summary(current_user: CurrentUser,service: StatisticsServiceInstance, period: Optional[PeriodType] = None):
    return await service.get_expense_summary(current_user, period)

@statistics_router.get("/incomes", response_model=IncomeSummary)
async def get_income_summary(current_user: CurrentUser,service: StatisticsServiceInstance, period: Optional[PeriodType] = None):
    return await service.get_income_summary(current_user, period)

@statistics_router.get("/overview", response_model=FinancialOverview)
async def get_financial_overview(current_user: CurrentUser, service: StatisticsServiceInstance, period: Optional[PeriodType] = None):
    return await service.get_financial_overview(current_user, period)