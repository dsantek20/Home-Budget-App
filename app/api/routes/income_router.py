
from uuid import UUID
from fastapi import APIRouter, Depends
from api.models.income_models import IncomeCreate, IncomeGet, IncomeUpdate
from services.income_service import IncomeServiceInstance
from auth.dependencies import CurrentUser, get_current_user


income_router = APIRouter(dependencies=[Depends(get_current_user)])

@income_router.get("/{income_id}", response_model=IncomeGet)
async def get_income_by_id(income_id: UUID, service: IncomeServiceInstance):
    return await service.get_income_by_id(income_id)

@income_router.post("/", response_model=IncomeGet)
async def create_new_income(current_user: CurrentUser, request: IncomeCreate, service: IncomeServiceInstance):
    return await service.create_new_income(current_user, request)

