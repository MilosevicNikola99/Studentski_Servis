from fastapi import HTTPException, Depends


from ..Repository.student_repository import StudentRepository,get_student_repository
from ..Schemas import schemas

def get_student_service(repo: StudentRepository = Depends(get_student_repository)):
    return StudentService(repo)

class StudentService:

    def __init__(self,repository : StudentRepository):
        self.student_repository = repository

    def create(self,student : schemas.StudentCreate):
        if self.student_repository.get_student_by_indeks(student.indeks):
            raise HTTPException(status_code=400,detail = "Student already exists")
        return self.student_repository.create_student(student)

    def get_by_id(self,student_id: int):
        student = self.student_repository.get_student_by_id(student_id)
        if student is None:
            raise HTTPException(status_code = 404,detail = "Student not found")

        return student

    def update(self,student: schemas.Student):
        student = self.student_repository.update_student(student)
        if student is None:
            raise HTTPException(status_code = 404 ,detail = "Student not found")
        return student


    def delete(self,student_id : int):
        response = self.student_repository.delete_student(student_id)
        if response is None:
            raise HTTPException(status_code = 404, detail = "Student not found")
        return response


