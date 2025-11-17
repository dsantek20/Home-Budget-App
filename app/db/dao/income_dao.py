from typing import Annotated
from fastapi import Depends
from db.dao.base_dao import BaseDAO
from db.database import DatabaseSession


class IncomeDao(BaseDAO):
    pass

def get_income_dao(session: DatabaseSession) -> IncomeDao:
    return IncomeDao(session)


IncomeDaoInstance = Annotated[IncomeDao, Depends(get_income_dao)]