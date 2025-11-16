
from uuid import UUID
from fastapi import APIRouter, Depends
from api.models.expense_models import ExpenseCreate, ExpenseGet, ExpenseUpdate
from services.expense_service import ExpenseServiceInstance
from auth.dependencies import CurrentUser, get_current_user


expense_router = APIRouter(dependencies=[Depends(get_current_user)])

@expense_router.get("/{expense_id}", response_model=ExpenseGet)
async def get_expense_by_id(expense_id: UUID, service: ExpenseServiceInstance):
    return await service.get_expense_by_id(expense_id)

@expense_router.post("/", response_model=ExpenseGet)
async def create_new_expense(current_user: CurrentUser, request: ExpenseCreate, service: ExpenseServiceInstance):
    return await service.create_new_expense(current_user, request)

@expense_router.patch("/{expense_id}", response_model=ExpenseGet)
async def update_expense(expense_id: UUID, request: ExpenseUpdate, service: ExpenseServiceInstance):
    return await service.update_expense(expense_id, request)