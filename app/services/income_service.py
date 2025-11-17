from typing import Annotated
from fastapi import Depends, status
from api.models.income_models import IncomeGet, IncomeCreate
from db.dao.income_dao import IncomeDao, IncomeDaoInstance
from db.entities.types.category_type import CategoryType
from db.entities.category_entities import Category
from error_handling.error_handling import ApplicationException
from db.entities.income_entities import Income
from db.entities.user_entities import User


class IncomeService:
    def __init__(self, dao: IncomeDao):
        self.dao = dao
    
    async def create_new_income(self, current_user: User, request: IncomeCreate) -> IncomeGet:
        category = await self.dao.get_by_id(Category, request.category_id)
    
        if category.category_type != CategoryType.INCOME.value:
            raise ApplicationException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Invalid category type",
                debug_message=f"Category must be of type INCOME, but got {category.category_type}",
                code="SVC-4002"
            )
        
        income = await self.dao.create(Income, **request.model_dump(), user_id=current_user.id)

        if income:
            current_user.balance = current_user.balance + request.amount
            await current_user.update(self.dao.session)
        return IncomeGet.model_validate(income)

def get_income_service(dao: IncomeDaoInstance) -> IncomeService:
    return IncomeService(dao)


IncomeServiceInstance = Annotated[IncomeService, Depends(get_income_service)]
