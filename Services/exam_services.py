from datetime import datetime
from fastapi import HTTPException,Depends

from ..Schemas import schemas
from ..Repository.exam_repository import ExamRepository,get_exam_repository

def get_exam_service(repo : ExamRepository = Depends(get_exam_repository)):
    return ExamServices(repo)

class ExamServices:
    def __init__(self,exam_repository):
        self.exam_repository = exam_repository

    def get_exam(self, student_id, sifra_predmeta, datum,username: str):
        if self.exam_repository.is_admin(username) or self.exam_repository.is_student(student_id,username) or self.exam_repository.is_professor(username):
            exam = self.exam_repository.get_exam( student_id, sifra_predmeta, datum)
            if exam is None:
                raise HTTPException(status_code=404,detail="Course not found")
            return exam
        else:
            raise HTTPException(status_code=401,detail="You are not authorized to get this exam")


    def create(self,  exam: schemas.ExamCreate, username : str):
        if self.exam_repository.is_admin(username) or self.exam_repository.is_professor(username):
            if self.exam_repository.get_exam( exam.student_id,exam.sifra_predmeta,exam.datum):
                raise HTTPException(status_code=400,detail="Course already exists")
            return self.exam_repository.create_exam( exam)
        else:
            raise HTTPException(status_code=401,detail="You are not authorized to create exam")

    def delete(self, student_id:int , sifra_predmeta: str ,datum : datetime, username : str):
        if self.exam_repository.is_admin(username) or self.exam_repository.is_professor(username):
            response = self.exam_repository.delete_exam( student_id,sifra_predmeta,datum)
            if response is None:
                raise HTTPException(status_code=404,detail="Course not found")
            return response
        else:
            raise HTTPException(status_code=401,detail="You are not authorized to delete exam")


    def update(self,  exam : schemas.Exam, username : str):
        if self.exam_repository.is_admin(username) or self.exam_repository.is_professor(username):
            exam = self.exam_repository.update_exam( exam)
            if exam is None:
                raise HTTPException(status_code=404,detail="Exam not found")
            return exam
        else:
            raise HTTPException(status_code=401,detail="You are not authorized to update exam")

