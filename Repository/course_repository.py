from fastapi import HTTPException,Depends
from ..dependencies import get_db

from ..Database import models ,database
from ..Schemas import schemas

def get_course_repository(db: database.SessionLocal = Depends(get_db)):
    return CourseRepository(db)


class CourseRepository:

    def __init__(self,db):
        self.db = db

    def get_course_by_sifra(self, sifra_predemta:str):
        return self.db.query(models.Course).filter(sifra_predemta == models.Course.sifra_predmeta).first()


    def create_course(self, course : schemas.Course):
        db_course = models.Course(sifra_predmeta=course.sifra_predmeta,naziv=course.naziv,espb=course.espb, profesor_id=course.profesor_id)
        try:
            self.db.add(db_course)
        except:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Course not created")

        self.db.commit()
        self.db.refresh(db_course)

        return db_course

    def delete_course(self, sifra_predmeta : str):
        course = self.get_course_by_sifra(sifra_predmeta)
        if course:
            try:
                self.db.delete(course)
            except:
                self.db.rollback()
                raise HTTPException(status_code=400, detail="Course not deleted")
            self.db.commit()
            return {"Course deleted" : True}
        return None


    def update_course(self, up_course : schemas.Course):
        course = self.db.query(models.Course).filter(up_course.sifra_predmeta == models.Course.sifra_predmeta).first()
        if course:
            try:
                course.naziv = up_course.naziv
                course.espb = up_course.espb
                course.profesor_id = up_course.profesor_id
            except:
                self.db.rollback()
                raise HTTPException(status_code=400, detail="Course not updated")

            self.db.commit()
            self.db.refresh(course)
            return course
        return None