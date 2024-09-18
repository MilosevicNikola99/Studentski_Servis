from datetime import datetime
from fastapi import HTTPException

from sqlalchemy.orm import Session

from Database import models
from Schemas import schemas

def get_exam_by_sifra(db : Session, sifra_predemta:str):
    return db.query(models.Exam).filter(sifra_predemta == models.Exam.sifra_predmeta).first()


def get_exam(db : Session, student_id : int, sifra_predmeta : str, datum : datetime):
    return db.query(models.Exam).filter(student_id == models.Exam.student_id,
                                        sifra_predmeta == models.Exam.sifra_predmeta,
                                        datum == models.Exam.datum).first()


def create_exam(db: Session, exam : schemas.ExamCreate):
    db_exam = models.Exam(**exam.model_dump())

    try:
        db.add(db_exam)
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail='Database Error : create exam failed')

    db.commit()
    db.refresh(db_exam)
    return db_exam



def delete_exam(db: Session,student_id: int ,sifra_predmeta : str , datum : datetime):
    exam = get_exam(db,student_id,sifra_predmeta,datum)
    if exam:
        try:
            db.delete(exam)
        except:
            db.rollback()
            raise HTTPException(status_code=400, detail='Database Error : delete exam failed')
        db.commit()
        return {"Course deleted" : True}
    return None


def update_exam(db : Session, up_exam : schemas.Exam):
    exam = get_exam(db,up_exam.student_id, up_exam.sifra_predmeta, up_exam.datum)
    if exam:
        try:
            exam.datum = up_exam.datum
            exam.ocena = up_exam.ocena
            exam.polozen = up_exam.polozen
        except:
            db.rollback()
            raise HTTPException(status_code=400, detail='Database Error : update exam failed')

        db.commit()
        db.refresh(exam)
        return exam
    return None