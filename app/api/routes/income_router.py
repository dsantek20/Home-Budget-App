
from datetime import date
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from api.models.income_models import IncomeCreate, IncomeFilter, IncomeGet, IncomeUpdate
from services.income_service import IncomeServiceInstance
from auth.dependencies import CurrentUser, get_current_user


income_router = APIRouter(dependencies=[Depends(get_current_user)])

def get_income_filters(
    category_id: Optional[UUID] = Query(None, description="Filter by category"),
    min_amount: Optional[Decimal] = Query(None, ge=0, description="Minimum amount"),
    max_amount: Optional[Decimal] = Query(None, ge=0, description="Maximum amount"),
    start_date: Optional[date] = Query(None, alias="from", description="Start date"),
    end_date: Optional[date] = Query(None, alias="to", description="End date"),
    sort_by: Optional[str] = Query("income_date", enum=["income_date", "amount"]),
    sort_order: Optional[str] = Query("desc", enum=["asc", "desc"]),
    limit: Optional[int] = Query(None, ge=1, description="Max results")
):
    return {
        "category_id": category_id,
        "min_amount": min_amount,
        "max_amount": max_amount,
        "start_date": start_date,
        "end_date": end_date,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "limit": limit
    }

@income_router.get("/{income_id}", response_model=IncomeGet)
async def get_income_by_id(income_id: UUID, service: IncomeServiceInstance):
    return await service.get_income_by_id(income_id)

@income_router.get("/", response_model=List[IncomeGet])
async def get_incomes(current_user: CurrentUser, service: IncomeServiceInstance, filter_params: dict = Depends(get_income_filters)):
    filters = IncomeFilter(**filter_params)
    return await service.get_incomes(current_user, filters)

@income_router.post("/", response_model=IncomeGet)
async def create_new_income(current_user: CurrentUser, request: IncomeCreate, service: IncomeServiceInstance):
    return await service.create_new_income(current_user, request)

@income_router.patch("/{income_id}", response_model=IncomeGet)
async def update_income(income_id: UUID, current_user: CurrentUser, request: IncomeUpdate, service: IncomeServiceInstance):
    return await service.update_income(current_user, income_id, request)

@income_router.delete("/{income_id}")
async def delete_income(income_id: UUID, current_user: CurrentUser, service: IncomeServiceInstance):
    return await service.delete_income(current_user, income_id)

@income_router.delete("/{income_id}/permanent")
async def delete_income_permanently(income_id: UUID, current_user: CurrentUser, service: IncomeServiceInstance):
    return await service.delete_income_permanently(current_user, income_id)