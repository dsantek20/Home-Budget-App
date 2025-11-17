from sqlalchemy import UUID, Boolean, Column, ForeignKey, String
from db.entities.types.category_type import CategoryType
from utils.db_validators import valid_enum
from db.entities.base_model import BaseUUIDModel
from sqlalchemy.orm import relationship, validates


class Category(BaseUUIDModel):
    __tablename__ = "categories"

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_predefined = Column(Boolean, default=False)
    category_type = Column(String, nullable=False, default="EXPENSE")

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    user = relationship("User", back_populates="categories", lazy="selectin")

    expenses = relationship(
        "Expense",
        back_populates="category",
        lazy="selectin",
    )

    @valid_enum(CategoryType)
    @validates("category_type")
    def validate_status(self, key, value):
        return value
