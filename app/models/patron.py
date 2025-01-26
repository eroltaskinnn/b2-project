from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from core.database import Base
from .common import CommonModel


class Patron(CommonModel):
    __tablename__ = "patrons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)

    checkouts = relationship("Checkout", back_populates="patron")


# metadata = Base.metadata

