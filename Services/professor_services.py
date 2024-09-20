from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..Schemas import schemas
from ..Repository import professor_repository


def create(db : Session, professor : schemas.ProfessorCreate):
    if professor_repository.get_professor(db, professor):
        raise HTTPException(status_code=400,detail="Professor already exists")
    return professor_repository.create_professor(db, professor)


def get_by_id(db, id):
    professor =  professor_repository.get_professor_by_id(db, id)
    if professor is None:
        raise HTTPException(status_code=404,detail="Professor not found")
    return professor


def update(db, professor : schemas.Professor):
    professor = professor_repository.update_professor(db, professor)
    if professor is None:
        raise HTTPException(status_code=404,detail="Professor not found")
    return professor


def delete(db, id):
    response = professor_repository.delete_professor(db, id)
    if response is None:
        raise HTTPException(status_code=404,detail="Professor not found")
    return response