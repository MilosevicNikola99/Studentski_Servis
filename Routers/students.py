from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from Database import  models , database
from Schemas import schemas
from Services import student_services

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/students/",response_model=schemas.Student)
def create_student(student: schemas.StudentCreate ,db: Session = Depends(get_db)):
    return student_services.create(db,student)

@app.get("/students/{id}",response_model=schemas.Student)
def get_student_by_id(id:int,db: Session = Depends(get_db)):
    return student_services.get_by_id(db,id)

@app.put("/students/{id}",response_model=schemas.Student)
def update_student(id : int, student: schemas.StudentBase,db: Session = Depends(get_db)):
    return student_services.update(db, schemas.Student(id = id,**student.model_dump()))

@app.delete("/students/{id}")
def delete_student(id: int,db: Session = Depends(get_db)):
    return student_services.delete(db,id)