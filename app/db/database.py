
import logging
from typing import Annotated, AsyncGenerator
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends
from error_handling.error_handling import ApplicationException
from app_config import get_app_config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(get_app_config().database_url)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

log = logging.getLogger(__name__)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()

        except SQLAlchemyError as e:
            await session.rollback()
            log.error(f"Database error occurred: {e}")
            raise ApplicationException(status_code=500, code="SVC-5002", message="Unable to retrieve data from database", debug_message=str(e))


DatabaseSession = Annotated[AsyncSession, Depends(get_session)]
