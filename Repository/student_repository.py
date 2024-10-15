from fastapi import HTTPException
from fastapi import Depends
from ..dependencies import get_db

from ..Database import models
from ..Schemas import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

def get_student_repository(db: AsyncSession = Depends(get_db)):
    return StudentRepository(db)

class StudentRepository:

    def __init__(self,db : AsyncSession):
        self.db = db

    async def create_student(self,student : schemas.StudentCreate):
        db_student = models.Student(ime=student.ime,prezime=student.prezime,indeks=student.indeks,user_id = student.user_id)
        try:
            self.db.add(db_student)
            await self.db.commit()
        except:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail='Database Error : create student failed')

        await self.db.refresh(db_student)
        return db_student

    async def get_student_by_id(self, student_id : int):
        stmt = select(models.Student).filter(models.Student.id == student_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


    async def get_student_by_indeks(self, indeks : str):
        stmt = select(models.Student).filter(models.Student.indeks == indeks)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update_student(self,up_student : schemas.Student):
        stmt = select(models.Student).filter(models.Student.id == up_student.id)
        result = await self.db.execute(stmt)
        student = result.scalar_one_or_none()
        if student:
            try:
                student.ime = up_student.ime
                student.prezime = up_student.prezime
                student.indeks = up_student.indeks
                await self.db.commit()
            except:
                await self.db.rollback()
                raise HTTPException(status_code=400, detail='Database Error: update student failed')

            await self.db.refresh(student)
            return student
        return None


    async def delete_student(self, student_id : int):
        stmt = select(models.Student).filter(models.Student.id == student_id)
        result = await self.db.execute(stmt)
        student = result.scalar_one_or_none()
        if student:
            try:
                await self.db.delete(student)
                await self.db.commit()
            except:
                await self.db.rollback()
                raise HTTPException(status_code=400, detail='Database Error: delete student failed')
            return {"Student deleted": True}
        return None


