from typing import Annotated
from fastapi import Depends
from db.dao.base_dao import BaseDAO
from db.database import DatabaseSession


class ExpenseDao(BaseDAO):
    pass

def get_expense_dao(session: DatabaseSession) -> ExpenseDao:
    return ExpenseDao(session)


ExpenseDaoInstance = Annotated[ExpenseDao, Depends(get_expense_dao)]