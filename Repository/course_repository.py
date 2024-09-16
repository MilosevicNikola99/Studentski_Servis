from sqlalchemy.orm import Session

from Database import models
from Schemas import schemas

def get_course_by_sifra(db : Session, sifra_predemta:str):
    return db.query(models.Course).filter(sifra_predemta == models.Course.sifra_predmeta).first()


def create_course(db: Session, course : schemas.Course):
    db_course = models.Course(sifra_predmeta=course.sifra_predmeta,naziv=course.naziv,espb=course.espb)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def delete_course(db: Session,sifra_predmeta : str):
    course = get_course_by_sifra(db,sifra_predmeta)
    if course:
        db.delete(course)
        db.commit()
        return {"Course deleted" : True}
    return None


def update_course(db : Session, up_course : schemas.Course):
    course = db.query(models.Course).filter(up_course.sifra_predmeta == models.Course.sifra_predmeta).first()
    if course:
        course.naziv = up_course.naziv
        course.espb = up_course.espb
        db.commit()
        db.refresh(course)
        return course
    return None