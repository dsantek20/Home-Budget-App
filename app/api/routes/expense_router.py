
from fastapi import APIRouter, Depends
from api.models.expense_models import ExpenseCreate, ExpenseGet
from services.expense_service import ExpenseServiceInstance
from auth.dependencies import CurrentUser, get_current_user


expense_router = APIRouter(dependencies=[Depends(get_current_user)])

@expense_router.post("/", response_model=ExpenseGet)
async def create_new_expense(current_user: CurrentUser, request: ExpenseCreate, service: ExpenseServiceInstance):
    return await service.create_new_expense(current_user, request)