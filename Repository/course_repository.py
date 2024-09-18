from fastapi import HTTPException
from sqlalchemy.orm import Session

from Database import models
from Schemas import schemas

def get_course_by_sifra(db : Session, sifra_predemta:str):
    return db.query(models.Course).filter(sifra_predemta == models.Course.sifra_predmeta).first()


def create_course(db: Session, course : schemas.Course):
    db_course = models.Course(sifra_predmeta=course.sifra_predmeta,naziv=course.naziv,espb=course.espb)
    try:
        db.add(db_course)
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Course not created")

    db.commit()
    db.refresh(db_course)

    return db_course

def delete_course(db: Session,sifra_predmeta : str):
    course = get_course_by_sifra(db,sifra_predmeta)
    if course:
        try:
            db.delete(course)
        except:
            db.rollback()
            raise HTTPException(status_code=400, detail="Course not deleted")
        db.commit()
        return {"Course deleted" : True}
    return None


def update_course(db : Session, up_course : schemas.Course):
    course = db.query(models.Course).filter(up_course.sifra_predmeta == models.Course.sifra_predmeta).first()
    if course:
        try:
            course.naziv = up_course.naziv
            course.espb = up_course.espb
        except:
            db.rollback()
            raise HTTPException(status_code=400, detail="Course not updated")

        db.commit()
        db.refresh(course)
        return course
    return None