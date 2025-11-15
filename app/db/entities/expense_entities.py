from sqlalchemy import UUID, Column, DateTime, ForeignKey, Numeric, String
from utils.datetime_helpers import get_current_datetime
from db.entities.base_model import BaseUUIDModel
from sqlalchemy.orm import relationship


class Expense(BaseUUIDModel):
    __tablename__ = "expenses"

    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    description = Column(String, nullable=False)
    expense_date = Column(DateTime(timezone=True), default=get_current_datetime, nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="expenses", lazy="selectin")

    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False)
    category = relationship("Category", back_populates="expenses", lazy="selectin")
