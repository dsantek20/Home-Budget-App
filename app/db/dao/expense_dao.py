from typing import Annotated, List
from uuid import UUID
from fastapi import Depends
from sqlalchemy import select, asc, desc
from api.models.expense_models import ExpenseFilter
from utils.datetime_helpers import get_current_datetime
from db.entities.expense_entities import Expense
from db.dao.base_dao import BaseDAO
from db.database import DatabaseSession


class ExpenseDao(BaseDAO):

    async def get_filtered_expenses(self, user_id: UUID, filters: ExpenseFilter) -> List[Expense]:
        query = select(Expense).where(
            Expense.user_id == user_id,
            Expense.deleted_at.is_(None)
        )
        
        if filters.category_id:
            query = query.where(Expense.category_id == filters.category_id)
        if filters.min_amount:
            query = query.where(Expense.amount >= filters.min_amount)
        if filters.max_amount:
            query = query.where(Expense.amount <= filters.max_amount)
        if filters.start_date:
            query = query.where(Expense.expense_date >= filters.start_date)
        if filters.end_date:
            query = query.where(Expense.expense_date <= filters.end_date)
        
        sort_column = getattr(Expense, filters.sort_by, Expense.expense_date)
        sort_function = desc if filters.sort_order == "desc" else asc
        query = query.order_by(sort_function(sort_column))

        if filters.limit:
            query = query.limit(filters.limit)
        
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_expense(self, expense: Expense, update_obj) -> Expense:
        if not expense:
            return None
        
        update_data = update_obj.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            if hasattr(expense, key):
                setattr(expense, key, value)
        
        await expense.update(self.session)
        return expense
    
    async def delete_expense_by_id(self, expense: Expense, force: bool = False) -> None:
        if expense is None:
            return

        if force:
            await self.session.delete(expense)
            await self.session.commit()
        else:
            if expense.deleted_at:
                return

            expense.deleted_at = get_current_datetime()
            await self.session.commit()

def get_expense_dao(session: DatabaseSession) -> ExpenseDao:
    return ExpenseDao(session)


ExpenseDaoInstance = Annotated[ExpenseDao, Depends(get_expense_dao)]