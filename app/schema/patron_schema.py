from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import  Session

from core.dependency import get_db
from models.book import Book
from models.checkout import Checkout
from models.patron import Patron

class PatronBase(BaseModel):
    name: str
    email: str


class PatronCreate(PatronBase):
    pass


class PatronResponse(PatronBase):
    id: int

    class Config:
        orm_mode = True
