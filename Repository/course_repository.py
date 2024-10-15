from fastapi import HTTPException,Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from ..dependencies import get_db

from ..Database import models
from ..Schemas import schemas

def get_course_repository(db: AsyncSession = Depends(get_db)):
    return CourseRepository(db)


class CourseRepository:

    def __init__(self,db : AsyncSession):
        self.db = db

    async def get_course_by_sifra(self, sifra_predemta:str):
        result = await self.db.execute(select(models.Course).options(selectinload(models.Course.profesor)).filter(models.Course.sifra_predmeta == sifra_predemta))
        return result.scalar_one_or_none()

    async def get_courses(self,profesor_id,naziv,departman):

        stmt = select(models.Course, models.Professor).join(models.Professor, models.Course.profesor_id == models.Professor.id)

        if profesor_id:
            stmt = stmt.filter(models.Course.profesor_id == profesor_id)
        if naziv:
            stmt = stmt.filter(models.Course.naziv == naziv)
        if departman:
            stmt = stmt.filter(models.Professor.departman == departman)

        result = await self.db.execute(stmt)
        return result.scalars().all()


    async def create_course(self, course : schemas.Course):
        db_course = models.Course(sifra_predmeta=course.sifra_predmeta,naziv=course.naziv,espb=course.espb, profesor_id=course.profesor_id)
        try:
            self.db.add(db_course)
        except:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Course not created")

        await self.db.commit()
        await self.db.refresh(db_course)

        return db_course

    async def delete_course(self, sifra_predmeta : str):
        course = await self.get_course_by_sifra(sifra_predmeta)
        if course:
            try:
                await self.db.delete(course)
            except:
                await self.db.rollback()
                raise HTTPException(status_code=400, detail="Course not deleted")
            await self.db.commit()
            return {"Course deleted" : True}
        return None


    async def update_course(self, up_course : schemas.CourseBase,sifra_predmeta : str):

        result = await (self.db.execute(select(models.Course).filter(models.Course.sifra_predmeta == sifra_predmeta)))
        course = result.scalar_one_or_none()
        if course:
            try:
                course.naziv = up_course.naziv
                course.espb = up_course.espb
                course.profesor_id = up_course.profesor_id
            except:
                await self.db.rollback()
                raise HTTPException(status_code=400, detail="Course not updated")

            await self.db.commit()
            await self.db.refresh(course)
            return course
        return None

