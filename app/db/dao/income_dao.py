from typing import Annotated, List
from uuid import UUID
from fastapi import Depends
from sqlalchemy import asc, desc, select
from api.models.income_models import IncomeFilter
from utils.datetime_helpers import get_current_datetime
from db.entities.income_entities import Income
from db.dao.base_dao import BaseDAO
from db.database import DatabaseSession


class IncomeDao(BaseDAO):

    async def get_filtered_incomes(self, user_id: UUID, filters: IncomeFilter) -> List[Income]:
        query = select(Income).where(
            Income.user_id == user_id,
            Income.deleted_at.is_(None)
        )
        
        if filters.category_id:
            query = query.where(Income.category_id == filters.category_id)
        if filters.min_amount:
            query = query.where(Income.amount >= filters.min_amount)
        if filters.max_amount:
            query = query.where(Income.amount <= filters.max_amount)
        if filters.start_date:
            query = query.where(Income.income_date >= filters.start_date)
        if filters.end_date:
            query = query.where(Income.income_date <= filters.end_date)
        
        sort_column = getattr(Income, filters.sort_by, Income.income_date)
        sort_function = desc if filters.sort_order == "desc" else asc
        query = query.order_by(sort_function(sort_column))

        if filters.limit:
            query = query.limit(filters.limit)
        
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_income(self, income: Income, update_obj) -> Income:
        if not income:
            return None
        
        update_data = update_obj.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            if hasattr(income, key):
                setattr(income, key, value)
        
        await income.update(self.session)
        return income

    async def delete_income_by_id(self, income: Income, force: bool = False) -> None:
        if income is None:
            return

        if force:
            await self.session.delete(income)
            await self.session.commit()
        else:
            if income.deleted_at:
                return

            income.deleted_at = get_current_datetime()
            await self.session.commit()

def get_income_dao(session: DatabaseSession) -> IncomeDao:
    return IncomeDao(session)


IncomeDaoInstance = Annotated[IncomeDao, Depends(get_income_dao)]