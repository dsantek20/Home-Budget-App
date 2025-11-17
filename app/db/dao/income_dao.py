from typing import Annotated
from fastapi import Depends
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

def get_income_dao(session: DatabaseSession) -> IncomeDao:
    return IncomeDao(session)


IncomeDaoInstance = Annotated[IncomeDao, Depends(get_income_dao)]