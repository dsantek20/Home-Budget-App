from sqlalchemy import Column, String
from db.entities.base_model import BaseUUIDModel


class User(BaseUUIDModel):
    __tablename__ = "user"

    email = Column(String, nullable=False, unique=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
