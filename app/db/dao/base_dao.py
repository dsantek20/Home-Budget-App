from typing import Optional, Type, TypeVar
from db.entities.base_model import BaseUUIDModel


T = TypeVar("T", bound=BaseUUIDModel)


class BaseDAO:

    def __init__(self, session):
        self.session = session

    async def run_query(self, query):
        return await self.session.execute(query)
    

    async def create(self, model: Type[T], **kwargs) -> Optional[T]:
        obj = model(**kwargs)
        await obj.save(self.session)
        return obj