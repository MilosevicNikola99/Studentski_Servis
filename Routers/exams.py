from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException , APIRouter
from sqlalchemy.orm import Session


from ..Database import  models , database
from ..Schemas import schemas
from ..Services import  exam_services
from ..dependencies import get_db

models.Base.metadata.create_all(bind=database.engine)

router = APIRouter()

@router.post("/exams/")
def create_course(exam: schemas.ExamCreate , db : Session = Depends(get_db)):
    return exam_services.create(db, exam)

@router.get("/exams/{student_id}/{sifra_predmeta}/{datum}")
def get_exam(student_id:int , sifra_predmeta:str , datum :datetime, db : Session = Depends(get_db)):
    return exam_services.get_exam(student_id,sifra_predmeta,datum,db)

@router.put("/exams/{student_id}/{sifra_predmeta}/{datum}")
def update_course(student_id:int , sifra_predmeta:str , datum :datetime ,exam : schemas.ExamBase , db : Session = Depends(get_db)):
    exam = exam.model_dump()
    return exam_services.update(db, schemas.Exam(student_id=student_id,sifra_predmeta=sifra_predmeta,datum = datum,ocena=exam["ocena"],polozen=exam["polozen"]))

@router.delete("/exams/{student_id}/{sifra_predmeta}/{datum}")
def delete_course(student_id:int , sifra_predmeta:str , datum :datetime, db : Session = Depends(get_db)):
    return exam_services.delete(db, student_id , sifra_predmeta,datum)