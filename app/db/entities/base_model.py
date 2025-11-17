import uuid
from sqlalchemy import UUID, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column
from utils.datetime_helpers import get_current_datetime

class Base(DeclarativeBase):
    pass


class BaseUUIDModel(Base):
    __abstract__ = True 

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, sort_order=0)
    created_at = mapped_column(DateTime(timezone=True), default=get_current_datetime, nullable=False, sort_order=1)
    updated_at = mapped_column(DateTime(timezone=True), default=get_current_datetime, onupdate=get_current_datetime, nullable=False, sort_order=2)

    # Soft delete
    deleted_at = mapped_column(DateTime(timezone=True), nullable=True)

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()
        await session.refresh(self)

    async def update(self, session: AsyncSession):
        await session.commit()
        await session.refresh(self)