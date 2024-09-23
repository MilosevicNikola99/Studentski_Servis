from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..Database import models
from ..Schemas import schemas

def get_enrollments_by_id(db : Session, id : int):
    return db.query(models.Enrollment).filter(id == models.Enrollment.student_id).all()

def get_enrollments_by_sifra(db : Session, sifra_predmeta : str):
    return db.query(models.Enrollment).filter(sifra_predmeta == models.Enrollment.sifra_predmeta).all()


def get_enrollments_by_datum_upisa(db : Session, datum_upisa : datetime):
    return db.query(models.Enrollment).filter(datum_upisa == models.Enrollment.datum_upisa).all()



def get_enrollment(db : Session, student_id : int, sifra_predmeta : str, datum_upisa : datetime):
    return db.query(models.Enrollment).filter(student_id == models.Enrollment.student_id,
                                              sifra_predmeta == models.Enrollment.sifra_predmeta,
                                              datum_upisa == models.Enrollment.datum_upisa).first()

def get_enrollments(db):
    return db.query(models.Enrollment).all()

def create_enrollment(db : Session, enrollment : schemas.EnrolmentCreate):
    db_enrollment = models.Enrollment(student_id = enrollment.student_id,sifra_predmeta = enrollment.sifra_predmeta,datum_upisa = enrollment.datum_upisa)
    try:
        db.add(db_enrollment)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail='Database Error : create enrollment failed')

    db.refresh(db_enrollment)
    return db_enrollment


def update_enrollment(db, enrollment, up_enrollment):
    try:
        enrollment.student_id = up_enrollment.student_id
        enrollment.sifra_predmeta = up_enrollment.sifra_predmeta
        enrollment.datum_upisa = up_enrollment.datum_upisa
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail='Database Error : update enrollment failed')

    db.refresh(enrollment)
    return enrollment


def delete_enrollment(db, enrollment):
    try:
        db.delete(enrollment)
        db.commit()
        return { "Enrollment Deleted" : True}
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail='Database Error : delete enrollment failed')
