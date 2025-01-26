from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from core.database import Base

from .common import CommonModel

class Book(CommonModel):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    isbn = Column(String, unique=True)
    available = Column(Boolean, default=True)

    checkouts = relationship("Checkout", back_populates="book")

# metadata = Base.metadata

