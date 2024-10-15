from fastapi import Depends
from ..dependencies import get_db
from ..decorators import measure_time
from ..Database import models
from sqlalchemy  import select
from sqlalchemy import func , join
from sqlalchemy.sql import and_
from sqlalchemy.ext.asyncio import AsyncSession
import time

def get_statistics_repository(db: AsyncSession = Depends(get_db)):
    return StatisticsRepository(db)

class StatisticsRepository:

    def __init__(self,db : AsyncSession):
        self.db = db

    @measure_time
    async def get_sum_espb_for_student(self, student_id: int) -> int:
        stmt = (
            select(func.sum(models.Course.espb))
            .select_from(
                join(models.Exam, models.Course, models.Exam.sifra_predmeta == models.Course.sifra_predmeta)
            )
            .where(
                and_(
                    models.Exam.student_id == student_id,
                    models.Exam.polozen == True
                )
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar()

    async def count_passed_exams(self, student_id: int):
        stmt = (
            select(func.count())
            .select_from(
                join(models.Exam, models.Course, models.Exam.sifra_predmeta == models.Course.sifra_predmeta)
            )
            .where(
                and_(
                    models.Exam.student_id == student_id,
                    models.Exam.polozen == True
                )
            )
        )

        result = await  self.db.execute(stmt)

        return result.scalar()



