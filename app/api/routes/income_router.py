
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

@income_router.patch("/{income_id}", response_model=IncomeGet)
async def update_income(income_id: UUID, current_user: CurrentUser, request: IncomeUpdate, service: IncomeServiceInstance):
    return await service.update_income(current_user, income_id, request)

@income_router.delete("/{income_id}")
async def delete_income(income_id: UUID, current_user: CurrentUser, service: IncomeServiceInstance):
    return await service.delete_income(current_user, income_id)

@income_router.delete("/{income_id}/permanent")
async def delete_income_permanently(income_id: UUID, current_user: CurrentUser, service: IncomeServiceInstance):
    return await service.delete_income_permanently(current_user, income_id)