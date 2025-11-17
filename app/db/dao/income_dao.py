from typing import Annotated
from fastapi import Depends
from utils.datetime_helpers import get_current_datetime
from db.entities.income_entities import Income
from db.dao.base_dao import BaseDAO
from db.database import DatabaseSession


class IncomeDao(BaseDAO):

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