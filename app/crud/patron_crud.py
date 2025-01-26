from sqlalchemy.orm import Session
from models.patron import Patron
from schema.patron_schema import PatronCreate, PatronResponse
from fastapi import HTTPException


class PatronCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_patron(self, patron: PatronCreate):
        db_patron = Patron(**patron.dict())
        self.db.add(db_patron)
        self.db.commit()
        self.db.refresh(db_patron)
        return db_patron

    def read_patrons(self):
        return self.db.query(Patron).all()

    def read_patron(self, patron_id: int):
        patron = self.db.query(Patron).filter(Patron.id == patron_id).first()
        if patron is None:
            raise HTTPException(status_code=404, detail="Patron not found")
        return patron

    def update_patron(self, patron_id: int, patron: PatronCreate):
        db_patron = self.db.query(Patron).filter(Patron.id == patron_id).first()
        if db_patron is None:
            raise HTTPException(status_code=404, detail="Patron not found")

        for key, value in patron.dict().items():
            setattr(db_patron, key, value)

        self.db.commit()
        self.db.refresh(db_patron)
        return db_patron

    def delete_patron(self, patron_id: int):
        patron = self.db.query(Patron).filter(Patron.id == patron_id).first()
        if patron is None:
            raise HTTPException(status_code=404, detail="Patron not found")

        self.db.delete(patron)
        self.db.commit()
        return {"message": "Patron deleted successfully"}