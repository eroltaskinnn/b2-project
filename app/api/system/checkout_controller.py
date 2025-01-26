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
from schema.checkout_schema import CheckoutResponse, CheckoutCreate
from crud.checkout_crud import CheckoutCRUD


router = APIRouter()


# Checkout Operations
@router.post("/checkouts/", response_model=CheckoutResponse)
def checkout_book(checkout: CheckoutCreate, db: Session = Depends(get_db)):
    checkout_crud = CheckoutCRUD(db)
    return checkout_crud.checkout_book(checkout)


@router.get("/checkouts/current", response_model=List[CheckoutResponse])
def get_checked_out_books(db: Session = Depends(get_db)):
    checkout_crud = CheckoutCRUD(db)
    return checkout_crud.get_checked_out_books()


@router.get("/checkouts/overdue", response_model=List[CheckoutResponse])
def get_overdue_books(db: Session = Depends(get_db)):
    checkout_crud = CheckoutCRUD(db)
    return checkout_crud.get_overdue_books()


@router.post("/checkouts/{checkout_id}/return")
def return_book(checkout_id: int, db: Session = Depends(get_db)):
    checkout_crud = CheckoutCRUD(db)
    return checkout_crud.return_book(checkout_id)