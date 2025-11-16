
from typing import Annotated
from uuid import UUID
from fastapi import Depends, Response, status
from api.models.auth_models import UserGet
from api.models.expense_models import ExpenseCreate, ExpenseGet, ExpenseUpdate
from db.entities.expense_entities import Expense
from db.dao.expense_dao import ExpenseDao, ExpenseDaoInstance


class ExpenseService:
    def __init__(self, dao: ExpenseDao):
        self.dao = dao
    
    async def get_expense_by_id(self, expense_id: UUID) -> ExpenseGet:
        expense = await self.dao.get_by_id(Expense, expense_id)
        return ExpenseGet.model_validate(expense)
    
    async def create_new_expense(self, current_user: UserGet, request: ExpenseCreate) -> ExpenseGet:
        expense = await self.dao.create(Expense, **request.model_dump(), user_id=current_user.id)
        return ExpenseGet.model_validate(expense)
    
    async def update_expense(self, expense_id: UUID, request: ExpenseUpdate) -> ExpenseGet:
        expense_updated = await self.dao.update(Expense, expense_id, request)
        return ExpenseGet.model_validate(expense_updated)
    
    async def delete_expense(self, expense_id: UUID):
        await self.dao.delete_by_id(Expense, expense_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    async def delete_expense_permanently(self, expense_id: UUID):
        await self.dao.delete_by_id(Expense, expense_id, True)
        return Response(status_code=status.HTTP_204_NO_CONTENT)


def get_expense_service(dao: ExpenseDaoInstance) -> ExpenseService:
    return ExpenseService(dao)


ExpenseServiceInstance = Annotated[ExpenseService, Depends(get_expense_service)]
