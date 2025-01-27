from typing import List

from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlalchemy.orm import  Session

from core.dependency import get_db
from schema.patron_schema import PatronCreate, PatronResponse
from crud.patron_crud import PatronCRUD


router = APIRouter()


# Patron Operations
@router.post("/patrons/", response_model=PatronResponse)
def create_patron(patron: PatronCreate, db: Session = Depends(get_db)):
    try:
        patron_crud = PatronCRUD(db)
        return patron_crud.create_patron(patron)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/patrons/", response_model=List[PatronResponse])
def read_patrons(db: Session = Depends(get_db)):
    try:
        patron_crud = PatronCRUD(db)
        return patron_crud.read_patrons()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/patrons/{patron_id}", response_model=PatronResponse)
def read_patron(patron_id: int, db: Session = Depends(get_db)):
    try:
        patron_crud = PatronCRUD(db)
        return patron_crud.read_patron(patron_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/patrons/{patron_id}", response_model=PatronResponse)
def update_patron(patron_id: int, patron: PatronCreate, db: Session = Depends(get_db)):
    try:
        patron_crud = PatronCRUD(db)
        return patron_crud.update_patron(patron_id, patron)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/patrons/{patron_id}")
def delete_patron(patron_id: int, db: Session = Depends(get_db)):
    try:
        patron_crud = PatronCRUD(db)
        return patron_crud.delete_patron(patron_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))