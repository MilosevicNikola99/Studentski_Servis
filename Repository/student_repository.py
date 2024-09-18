from dns.rdtypes.IN.HTTPS import HTTPS
from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..Database import models
from ..Schemas import schemas

def create_student(db : Session,student : schemas.StudentCreate):
    db_student = models.Student(ime=student.ime,prezime=student.prezime,indeks=student.indeks)
    try:
        db.add(db_student)
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail='Database Error : create student failed')

    db.commit()
    db.refresh(db_student)
    return db_student

def get_student_by_id(db : Session, student_id : int):
    return db.query(models.Student).filter(student_id == models.Student.id).first()


def get_student_by_indeks(db : Session, indeks : str):
    return db.query(models.Student).filter(indeks == models.Student.indeks).first()

def update_student(db : Session,up_student : schemas.Student):
    student = db.query(models.Student).filter(up_student.id == models.Student.id).first()
    if student:
        try:
            student.ime = up_student.ime
            student.prezime = up_student.prezime
            student.indeks = up_student.indeks
        except:
            db.rollback()
            raise HTTPException(status_code=400, detail='Database Error : update student failed')

        db.commit()
        db.refresh(student)
        return student
    return None


def delete_student(db: Session, id : int):
    student = db.query(models.Student).filter(id == models.Student.id).first()
    if student:
        try:
            db.delete(student)
        except:
            db.rollback()
            raise HTTPException(status_code=400, detail='Database Error : delete student failed')
        db.commit()
        return {"Student deleted" : True}
    return None