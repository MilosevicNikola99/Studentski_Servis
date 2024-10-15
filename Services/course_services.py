from fastapi import HTTPException,Depends
from ..Repository.course_repository import CourseRepository, get_course_repository
from ..Schemas import schemas
from ..Services import permissions

def get_course_service(repo: CourseRepository = Depends(get_course_repository)):
    return CourseServices(repo)

class CourseServices:

    def __init__(self,course_repository):
        self.course_repository = course_repository

    async def create(self, course: schemas.CourseCreate,username : str):
        is_admin = await permissions.is_admin(username,self.course_repository.db)
        if not is_admin:
            raise HTTPException(status_code=403, detail="You are not authorized to create course")

        if await self.course_repository.get_course_by_sifra( course.sifra_predmeta):
            raise HTTPException(status_code=400,detail="Course already exists")
        return await self.course_repository.create_course( course)

    async def delete(self, sifra_predmeta: str,username : str):
        is_admin = await  permissions.is_admin(username,self.course_repository.db)
        if not is_admin:
            raise HTTPException(status_code=403, detail="You are not authorized to create course")
        response = await self.course_repository.delete_course(sifra_predmeta)
        if response is None:
            raise HTTPException(status_code=404,detail="Course not found")
        return response

    async def get_courses(self, profesor_id, naziv, departman):
        courses =  await self.course_repository.get_courses(profesor_id, naziv, departman)
        if courses is None:
            raise HTTPException(status_code=404,detail="Course not found")
        return courses

    async def get_by_sifra(self, sifra_predmeta : str):
        course = await self.course_repository.get_course_by_sifra(sifra_predmeta)
        if course is None:
            raise HTTPException(status_code=404,detail="Course not found")
        return course


    async def update(self, course : schemas.CourseBase,sifra_predmeta : str,username : str):
        is_admin =  await permissions.is_admin(username,self.course_repository.db)
        if not is_admin:
            raise HTTPException(status_code=403, detail="You are not authorized to create course")

        course = await self.course_repository.update_course( course , sifra_predmeta)
        if course is None:
            raise HTTPException(status_code=404,detail="Course not found")
        return course
