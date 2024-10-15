from datetime import datetime
from fastapi import HTTPException , Depends
from sqlalchemy import select

from ..dependencies import get_db
from ..Database import models
from ..Schemas import schemas
from sqlalchemy.ext.asyncio import AsyncSession

def get_exam_repository(db: AsyncSession = Depends(get_db)):
    return ExamRepository(db)

class ExamRepository:

    def __init__(self,db : AsyncSession):
        self.db = db

    async def get_exam_by_sifra(self, sifra_predemta:str):
        result = await self.db.execute(select(models.Exam).filter(models.Exam.sifra_predmeta == sifra_predemta))
        exam = result.scalar_one_or_none()
        return exam


    async def get_exam(self, student_id : int, sifra_predmeta : str, datum : datetime):
        result = await self.db.execute(select(models.Exam).filter(models.Exam.student_id == student_id,
                                                                  models.Exam.sifra_predmeta == sifra_predmeta,
                                                                  models.Exam.datum == datum))
        exam = result.scalar_one_or_none()
        return exam


    async def create_exam(self, exam : schemas.ExamCreate):
        db_exam = models.Exam(**exam.model_dump())

        try:
            self.db.add(db_exam)
        except:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail='Database Error : create exam failed')

        await self.db.commit()
        await self.db.refresh(db_exam)
        return db_exam



    async def delete_exam(self, student_id: int ,sifra_predmeta : str , datum : datetime):
        exam = await self.get_exam(student_id,sifra_predmeta,datum)
        if exam:
            try:
                await self.db.delete(exam)
            except:
                await self.db.rollback()
                raise HTTPException(status_code=400, detail='Database Error : delete exam failed')
            await self.db.commit()
            return {"Exam deleted" : True}
        return None


    async def update_exam(self, up_exam : schemas.Exam):
        exam = await self.get_exam(up_exam.student_id, up_exam.sifra_predmeta, up_exam.datum)
        if exam:
            try:
                exam.datum = up_exam.datum
                exam.ocena = up_exam.ocena
                exam.polozen = up_exam.polozen
            except:
                await self.db.rollback()
                raise HTTPException(status_code=400, detail='Database Error : update exam failed')

            await self.db.commit()
            await self.db.refresh(exam)
            return exam
        return None

