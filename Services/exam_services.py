from datetime import datetime

from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session

from ..Schemas import schemas
from ..Repository.exam_repository import ExamRepository,get_exam_repository

def get_exam_service(repo : ExamRepository = Depends(get_exam_repository)):
    return ExamServices(repo)

class ExamServices:
    def __init__(self,exam_repository):
        self.exam_repository = exam_repository

    def get_exam(self, student_id, sifra_predmeta, datum):
        exam = self.exam_repository.get_exam( student_id, sifra_predmeta, datum)
        if exam is None:
            raise HTTPException(status_code=404,detail="Course not found")
        return exam


    def create(self,  exam: schemas.ExamCreate):
        if self.exam_repository.get_exam( exam.student_id,exam.sifra_predmeta,exam.datum):
            raise HTTPException(status_code=400,detail="Course already exists")
        return self.exam_repository.create_exam( exam)

    def delete(self, student_id:int , sifra_predmeta: str ,datum : datetime):
        response = self.exam_repository.delete_exam( student_id,sifra_predmeta,datum)
        if response is None:
            raise HTTPException(status_code=404,detail="Course not found")
        return response


    def update(self,  exam : schemas.Exam):
        exam = self.exam_repository.update_exam( exam)
        if exam is None:
            raise HTTPException(status_code=404,detail="Exam not found")
        return exam

