from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..Schemas import schemas
from ..Repository import student_repository

def create(db: Session ,student : schemas.StudentCreate):
    if student_repository.get_student_by_indeks(db,student.indeks):
        raise HTTPException(status_code=400,detail = "Student already exists")
    return student_repository.create_student(db,student)

def get_by_id(db: Session ,id: int):
    student = student_repository.get_student_by_id(db,id)
    if student is None:
        raise HTTPException(status_code = 404,detail = "Student not found")

    return student

def update(db:Session,student: schemas.Student):
    student = student_repository.update_student(db,student)
    if student is None:
        raise HTTPException(status_code = 404 ,detail = "Student not found")
    return student


def delete( db : Session,id):
    response = student_repository.delete_student(db,id)
    if response is None:
        raise HTTPException(status_code = 404, detail = "Student not found")
    return response
