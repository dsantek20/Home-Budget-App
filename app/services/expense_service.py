
from decimal import Decimal
from typing import Annotated, List
from uuid import UUID
from fastapi import Depends, Response, status
from api.models.expense_models import ExpenseCreate, ExpenseGet, ExpenseUpdate, ExpenseFilter
from db.entities.user_entities import User
from db.entities.expense_entities import Expense
from db.dao.expense_dao import ExpenseDao, ExpenseDaoInstance


class ExpenseService:
    def __init__(self, dao: ExpenseDao):
        self.dao = dao
    
    async def get_expense_by_id(self, expense_id: UUID) -> ExpenseGet:
        expense = await self.dao.get_by_id(Expense, expense_id)
        return ExpenseGet.model_validate(expense)
    
    async def get_expenses(self, current_user: User, filters: ExpenseFilter) -> List[ExpenseGet]:
        expenses = await self.dao.get_filtered_expenses(current_user.id, filters)
        return [ExpenseGet.model_validate(expense) for expense in expenses]
    
    async def create_new_expense(self, current_user: User, request: ExpenseCreate) -> ExpenseGet:
        expense = await self.dao.create(Expense, **request.model_dump(), user_id=current_user.id)
        if expense:
            current_user.balance = current_user.balance - request.amount
            await current_user.update(self.dao.session)
        return ExpenseGet.model_validate(expense)
    
    async def update_expense(self, current_user: User, expense_id: UUID, request: ExpenseUpdate) -> ExpenseGet:
        expense = await self.dao.get_by_id(Expense, expense_id)
        old_amount = expense.amount
        expense_updated = await self.dao.update_expense(expense, request)
        if expense_updated and request.amount and request.amount != old_amount:
            difference = request.amount - old_amount
            current_user.balance = current_user.balance - difference
            await current_user.update(self.dao.session)
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
