
from datetime import date
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from api.models.expense_models import ExpenseCreate, ExpenseFilter, ExpenseGet, ExpenseUpdate
from services.expense_service import ExpenseServiceInstance
from auth.dependencies import CurrentUser, get_current_user


expense_router = APIRouter(dependencies=[Depends(get_current_user)])

def get_expense_filters(
    category_id: Optional[UUID] = Query(None, description="Filter by category"),
    min_amount: Optional[Decimal] = Query(None, ge=0, description="Minimum amount"),
    max_amount: Optional[Decimal] = Query(None, ge=0, description="Maximum amount"),
    start_date: Optional[date] = Query(None, alias="from", description="Start date"),
    end_date: Optional[date] = Query(None, alias="to", description="End date"),
    sort_by: Optional[str] = Query("expense_date", enum=["expense_date", "amount"]),
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

@expense_router.get("/{expense_id}", response_model=ExpenseGet)
async def get_expense_by_id(expense_id: UUID, service: ExpenseServiceInstance):
    return await service.get_expense_by_id(expense_id)

@expense_router.get("/", response_model=List[ExpenseGet])
async def get_expenses(current_user: CurrentUser, service: ExpenseServiceInstance, filter_params: dict = Depends(get_expense_filters)):
    filters = ExpenseFilter(**filter_params)
    return await service.get_expenses(current_user, filters)

@expense_router.post("/", response_model=ExpenseGet)
async def create_new_expense(current_user: CurrentUser, request: ExpenseCreate, service: ExpenseServiceInstance):
    return await service.create_new_expense(current_user, request)

@expense_router.patch("/{expense_id}", response_model=ExpenseGet)
async def update_expense(expense_id: UUID, request: ExpenseUpdate, service: ExpenseServiceInstance):
    return await service.update_expense(expense_id, request)

@expense_router.delete("/{expense_id}")
async def delete_expense(expense_id: UUID, service: ExpenseServiceInstance):
    return await service.delete_expense(expense_id)

@expense_router.delete("/{expense_id}/permanent")
async def delete_expense_permanently(expense_id: UUID, service: ExpenseServiceInstance):
    return await service.delete_expense_permanently(expense_id)