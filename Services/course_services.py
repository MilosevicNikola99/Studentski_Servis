from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..Schemas import schemas
from ..Repository import course_repository


def create(db : Session, course: schemas.Course):
    if course_repository.get_course_by_sifra(db, course.sifra_predmeta):
        raise HTTPException(status_code=400,detail="Course already exists")
    return course_repository.create_course(db, course)

def delete(db : Session, sifra_predmeta: str):
    response = course_repository.delete_course(db, sifra_predmeta)
    if response is None:
        raise HTTPException(status_code=404,detail="Course not found")
    return response

def get_by_sifra(db : Session, sifra_predmeta : str):
    course = course_repository.get_course_by_sifra(db, sifra_predmeta)
    print(course)
    if course is None:
        raise HTTPException(status_code=404,detail="Course not found")
    return course


def update(db : Session, course : schemas.Course):
    course = course_repository.update_course(db, course)
    if course is None:
        raise HTTPException(status_code=404,detail="Course not found")
    return course