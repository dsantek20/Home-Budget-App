from typing import Annotated
from uuid import UUID
from fastapi import Depends, status
from api.models.income_models import IncomeGet, IncomeCreate, IncomeUpdate
from db.dao.income_dao import IncomeDao, IncomeDaoInstance
from db.entities.types.category_type import CategoryType
from db.entities.category_entities import Category
from error_handling.error_handling import ApplicationException
from db.entities.income_entities import Income
from db.entities.user_entities import User


class IncomeService:
    def __init__(self, dao: IncomeDao):
        self.dao = dao
    
    async def get_income_by_id(self, income_id: UUID) -> IncomeGet:
        income = await self.dao.get_by_id(Income, income_id)
        return IncomeGet.model_validate(income)
    
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

    async def update_income(self, current_user: User, income_id: UUID, request: IncomeUpdate) -> IncomeGet:
        if request.category_id:
            category = await self.dao.get_by_id(Category, request.category_id)
        
            if category.category_type != CategoryType.INCOME.value:
                raise ApplicationException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Invalid category type",
                    debug_message=f"Category must be of type INCOME, but got {category.category_type}",
                    code="SVC-4002"
                )
            
        income = await self.dao.get_by_id(Income, income_id)
        old_amount = income.amount
        income_updated = await self.dao.update_income(income, request)
        income_get = IncomeGet.model_validate(income_updated)

        if income_updated and request.amount and request.amount != old_amount:
            difference = request.amount - old_amount
            current_user.balance = current_user.balance + difference
            await current_user.update(self.dao.session)

        return income_get


def get_income_service(dao: IncomeDaoInstance) -> IncomeService:
    return IncomeService(dao)


IncomeServiceInstance = Annotated[IncomeService, Depends(get_income_service)]
