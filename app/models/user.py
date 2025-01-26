from sqlalchemy import Column, String, Enum

from core.database import Base
from .common import CommonModel


class User(CommonModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    test3 = Column(String, nullable=True)

    def __repr__(self):
        return f"{self.email}"


metadata = Base.metadata
