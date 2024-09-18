from fastapi import Depends, FastAPI ,APIRouter
from sqlalchemy.orm import Session

from ..Database import  models , database
from ..Schemas import schemas
from ..Services import student_services
from ..dependencies import get_db

models.Base.metadata.create_all(bind=database.engine)
router = APIRouter()



@router.post("/students/",response_model=schemas.Student)
async def create_student(student: schemas.StudentCreate ,db: Session = Depends(get_db)):
    return student_services.create(db,student)

@router.get("/students/{id}",response_model=schemas.Student)
async def get_student_by_id(id:int,db: Session = Depends(get_db)):
    return student_services.get_by_id(db,id)

@router.put("/students/{id}",response_model=schemas.Student)
async def update_student(id : int, student: schemas.StudentBase,db: Session = Depends(get_db)):
    return student_services.update(db, schemas.Student(id = id,**student.model_dump()))

@router.delete("/students/{id}")
async def delete_student(id: int,db: Session = Depends(get_db)):
    return student_services.delete(db,id)