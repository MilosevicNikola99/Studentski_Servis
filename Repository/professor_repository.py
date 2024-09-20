from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..Database import models
from ..Schemas import schemas

def get_professor(db, professor : schemas.ProfessorBase):
    return db.query(models.Professor).filter(models.Professor.ime == professor.ime,
                                             models.Professor.prezime == professor.prezime,
                                             models.Professor.departman == professor.departman).first()


def create_professor(db, professor : schemas.ProfessorCreate):
    db_professor = models.Professor(ime=professor.ime, prezime=professor.prezime,departman=professor.departman)
    try:
        db.add(db_professor)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Database error")
    db.refresh(db_professor)
    return db_professor


def get_professor_by_id(db, id):
    return db.query(models.Professor).filter(models.Professor.id == id).first()


def update_professor(db, up_professor):
    professor = get_professor_by_id(db, up_professor.id)
    if professor:
        try:
            professor.ime = up_professor.ime
            professor.prezime = up_professor.prezime
            professor.departman = up_professor.departman
            db.commit()
        except:
            db.rollback()
            raise HTTPException(status_code=400, detail="Database error")
        db.refresh(professor)
        return professor
    return None


def delete_professor(db, id):
    professor = get_professor_by_id(db, id)
    if professor:
        try:
            db.delete(professor)
            db.commit()
        except:
            db.rollback()
            raise HTTPException(status_code=400, detail="Database error")
        return {"Professor deleted" : True}
    return None