from fastapi import HTTPException,Depends
from ..Repository.course_repository import CourseRepository, get_course_repository
from ..Schemas import schemas


def get_course_service(repo: CourseRepository = Depends(get_course_repository)):
    return CourseServices(repo)

class CourseServices:

    def __init__(self,course_repository):
        self.course_repository = course_repository

    def create(self, course: schemas.Course):
        if self.course_repository.get_course_by_sifra( course.sifra_predmeta):
            raise HTTPException(status_code=400,detail="Course already exists")
        return self.course_repository.create_course( course)

    def delete(self, sifra_predmeta: str):
        response = self.course_repository.delete_course(sifra_predmeta)
        if response is None:
            raise HTTPException(status_code=404,detail="Course not found")
        return response

    def get_by_sifra(self, sifra_predmeta : str):
        course = self.course_repository.get_course_by_sifra( sifra_predmeta)
        print(course)
        if course is None:
            raise HTTPException(status_code=404,detail="Course not found")
        return course


    def update(self, course : schemas.Course):
        course = self.course_repository.update_course( course)
        if course is None:
            raise HTTPException(status_code=404,detail="Course not found")
        return course