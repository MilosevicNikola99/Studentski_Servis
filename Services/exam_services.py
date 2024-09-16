from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from Schemas import schemas
from Repository import exam_repository



def get_exam(student_id, sifra_predmeta, datum, db):
    exam = exam_repository.get_exam(db, student_id, sifra_predmeta, datum)
    if exam is None:
        raise HTTPException(status_code=404,detail="Course not found")
    return exam


def create(db : Session, exam: schemas.ExamCreate):
    if exam_repository.get_exam(db, exam.student_id,exam.sifra_predmeta,exam.datum):
        raise HTTPException(status_code=400,detail="Course already exists")
    return exam_repository.create_exam(db, exam)

def delete(db : Session,student_id:int , sifra_predmeta: str ,datum : datetime):
    response = exam_repository.delete_exam(db, student_id,sifra_predmeta,datum)
    if response is None:
        raise HTTPException(status_code=404,detail="Course not found")
    return response

# def get_by_sifra(db : Session, sifra_predmeta : str):
#     course = exam_repository.get_course_by_sifra(db, sifra_predmeta)
#     print(course)
#     if course is None:
#         raise HTTPException(status_code=404,detail="Course not found")
#     return course


def update(db : Session, exam : schemas.Exam):
    exam = exam_repository.update_exam(db, exam)
    if exam is None:
        raise HTTPException(status_code=404,detail="Exam not found")
    return exam

