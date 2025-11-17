from sqlalchemy import UUID, Column, Date, ForeignKey, Numeric, String
from utils.datetime_helpers import get_current_date
from db.entities.base_model import BaseUUIDModel
from sqlalchemy.orm import relationship


class Income(BaseUUIDModel):
    __tablename__ = "incomes"

    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    description = Column(String, nullable=False)
    income_date = Column(Date, default=get_current_date, nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="incomes", lazy="selectin")

    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False)
    category = relationship("Category", back_populates="incomes", lazy="selectin")
