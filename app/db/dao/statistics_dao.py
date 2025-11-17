from typing import Annotated, List
from uuid import UUID
from fastapi import Depends
from sqlalchemy import and_, select
from db.entities.expense_entities import Expense
from utils.datetime_helpers import get_current_date
from db.dao.base_dao import BaseDAO
from db.database import DatabaseSession


class StatisticsDao(BaseDAO):

    async def get_expenses(self, user_id: UUID, start_date) -> List[Expense]:
        query = select(Expense).where(
            Expense.user_id == user_id,
            Expense.deleted_at.is_(None)
        )
        
        if start_date:
            query = query.where(
                and_(
                    Expense.expense_date >= start_date,
                    Expense.expense_date <= get_current_date()
                )
            )
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
def get_statistics_dao(session: DatabaseSession) -> StatisticsDao:
    return StatisticsDao(session)


StatisticsDaoInstance = Annotated[StatisticsDao, Depends(get_statistics_dao)]