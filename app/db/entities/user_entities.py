from sqlalchemy import Column, String
from db.entities.base_model import BaseUUIDModel
from sqlalchemy.orm import relationship

class User(BaseUUIDModel):
    __tablename__ = "user"

    email = Column(String, nullable=False, unique=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    categories = relationship(
        "Category",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
