from fastapi import HTTPException, Depends

from ..Services import permissions
from ..Repository.student_repository import StudentRepository,get_student_repository
from ..Schemas import schemas

def get_student_service(repo: StudentRepository = Depends(get_student_repository)):
    return StudentService(repo)

class StudentService:

    def __init__(self,repository : StudentRepository):
        self.student_repository = repository

    async def create(self,student : schemas.StudentCreate,username):
        is_admin = await permissions.is_admin(username,self.student_repository.db)
        if not is_admin:
            raise HTTPException(status_code=403, detail="You are not authorized to create student")

        if await self.student_repository.get_student_by_indeks(student.indeks):
            raise HTTPException(status_code=400,detail = "Student already exists")
        return await self.student_repository.create_student(student)

    async def get_by_id(self,student_id: int, username : str):
        have_permission = await permissions.check_permission(student_id,username,self.student_repository.db)
        if not have_permission:
            raise HTTPException(status_code=403, detail="You are not authorized to access this resource")

        student = await self.student_repository.get_student_by_id(student_id)
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")

        return student

    async def update(self,student: schemas.Student,username : str):
        is_admin = await permissions.is_admin(username,self.student_repository.db)
        if not is_admin:
            raise HTTPException(status_code=403, detail="You are not authorized to update this student")

        student =await self.student_repository.update_student(student)
        if student is None:
            raise HTTPException(status_code = 404 ,detail = "Student not found")
        return student


    async def delete(self,student_id : int, username : str):
        is_admin = await permissions.is_admin(username,self.student_repository.db)
        if not is_admin:
            raise HTTPException(status_code=403, detail="You are not authorized to delete this student")

        response = await self.student_repository.delete_student(student_id)
        if response is None:
            raise HTTPException(status_code = 404, detail = "Student not found")
        return response


