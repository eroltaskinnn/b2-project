from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import  Session

from core.dependency import get_db
from core.logger import logger
from schema.checkout_schema import CheckoutResponse, CheckoutCreate
from crud.checkout_crud import CheckoutCRUD


router = APIRouter()



@router.get("/checkouts/")
def get_checked_out_books(db: Session = Depends(get_db)):
    try:
        checkout_crud = CheckoutCRUD(db)
        return checkout_crud.get_checked_out_books()
    except Exception as e:
        logger.info(f"Failed to get checked out books: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/checkouts/overdue")
def get_overdue_books(db: Session = Depends(get_db)):
    try:
        checkout_crud = CheckoutCRUD(db)
        return checkout_crud.get_overdue_books()
    except Exception as e:
        logger.info(f"Failed to get overdue books: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/checkouts/{checkout_id}/return")
def return_book(checkout_id: int, db: Session = Depends(get_db)):
    try:
        checkout_crud = CheckoutCRUD(db)
        return checkout_crud.return_book(checkout_id)
    except Exception as e:
        logger.info(f"Failed to return book: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/checkouts/", response_model=CheckoutResponse)
def checkout_book(checkout: CheckoutCreate, db: Session = Depends(get_db)):
    try:
        checkout_crud = CheckoutCRUD(db)
        return checkout_crud.checkout_book(checkout)
    except Exception as e:
        logger.info(f"Failed to checkout book: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))