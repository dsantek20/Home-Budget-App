from sqlalchemy import UUID, Boolean, Column, ForeignKey, String
from db.entities.base_model import BaseUUIDModel
from sqlalchemy.orm import relationship


class Category(BaseUUIDModel):
    __tablename__ = "categories"

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_predefined = Column(Boolean, default=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    user = relationship("User", back_populates="categories", lazy="selectin")
