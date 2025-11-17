from typing import Optional, Type, TypeVar
import uuid
from sqlalchemy import select
from fastapi import status
from utils.datetime_helpers import get_current_datetime
from error_handling.error_handling import ApplicationException
from db.entities.base_model import BaseUUIDModel


T = TypeVar("T", bound=BaseUUIDModel)


class BaseDAO:

    def __init__(self, session):
        self.session = session

    async def run_query(self, query):
        return await self.session.execute(query)
    
    async def get_by_id(self, model: Type[T], id: uuid.UUID, include_deleted: bool = False, raise_error: bool = True) -> Optional[T]:
        stmt = select(model).where(model.id == id)
        
        if not include_deleted:
            stmt = stmt.where(model.deleted_at.is_(None))

        result = await self.session.execute(stmt)
        obj = result.scalars().first()

        if not obj and raise_error:
            raise ApplicationException(message="Not found",
                                       debug_message=f"{model.__name__} not found for ID {id}", code="SVC-4000",
                                       status_code=status.HTTP_404_NOT_FOUND)

        return obj

    async def create(self, model: Type[T], **kwargs) -> Optional[T]:
        obj = model(**kwargs)
        await obj.save(self.session)
        return obj
    
    async def update(self, model: Type[T], id: uuid.UUID, update_obj) -> Optional[T]:
        obj = await self.get_by_id(model, id)
        
        if not obj:
            return None
        
        update_data = update_obj.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        
        await obj.update(self.session)
        return obj
    
    async def delete_by_id(self, model: Type[T], id: uuid.UUID, force: bool = False) -> None:
        obj = await self.get_by_id(model, id, include_deleted=True, raise_error=False)

        if obj is None:
            return

        if force:
            await self.session.delete(obj)
            await self.session.commit()
        else:
            if obj.deleted_at:
                return

            obj.deleted_at = get_current_datetime()
            await self.session.commit()
    