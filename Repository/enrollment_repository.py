from datetime import datetime
from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db
from ..Database import models
from ..Schemas import schemas

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_enrollment_repository(db: AsyncSession = Depends(get_db)):
    return EnrollmentRepository(db)

class EnrollmentRepository:

    def __init__(self , db : AsyncSession):
        self.db = db

    async def get_enrollments_by_id(self, student_id : int):
        result = await self.db.execute(select(models.Enrollment).filter(models.Enrollment.student_id == student_id))
        enrollments = result.fetchone()
        return enrollments

    async def get_enrollments_by_sifra(self, sifra_predmeta : str):
        result = await self.db.execute(select(models.Enrollment).filter(models.Enrollment.sifra_predmeta == sifra_predmeta))
        enrollments = result.fetchall()
        return enrollments

    async def get_enrollments_by_datum_upisa(self, datum_upisa : datetime):
        result = await self.db.execute(select( models.Enrollment).filter(models.Enrollment.datum_upisa == datum_upisa))
        enrollments = result.fetchall()
        return enrollments

    async def get_enrollment(self, student_id : int, sifra_predmeta : str, datum_upisa : datetime):
        result = await self.db.execute(select(models.Enrollment).filter(models.Enrollment.student_id == student_id,
                                                                        models.Enrollment.sifra_predmeta == sifra_predmeta,
                                                                        models.Enrollment.datum_upisa == datum_upisa))
        enrollments = result.fetchall()
        return enrollments

    async def get_enrollments(self):

        result = await self.db.execute(select(models.Enrollment))
        enrollments = result.scalars().all()
        return enrollments

    async def create_enrollment(self, enrollment : schemas.EnrolmentCreate):
        db_enrollment = models.Enrollment(student_id = enrollment.student_id,sifra_predmeta = enrollment.sifra_predmeta,datum_upisa = enrollment.datum_upisa)
        try:
            self.db.add(db_enrollment)
            await self.db.commit()
        except:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail='Database Error : create enrollment failed')
        await self.db.refresh(db_enrollment)
        return db_enrollment


    async def update_enrollment(self,student_id,sifra_predmeta,datum_upisa, up_enrollment):
        enrollment_result = await self.db.execute(select(models.Enrollment).filter(models.Enrollment.student_id == student_id,
                                                                        models.Enrollment.sifra_predmeta == sifra_predmeta,
                                                                        models.Enrollment.datum_upisa == datum_upisa))
        enrollment = enrollment_result.scalars().first()
        try:
            enrollment.student_id = up_enrollment.student_id
            enrollment.sifra_predmeta = up_enrollment.sifra_predmeta
            enrollment.datum_upisa = up_enrollment.datum_upisa
            await self.db.commit()
        except:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail='Database Error : update enrollment failed')
        await self.db.refresh(enrollment)
        return enrollment


    async def delete_enrollment(self, student_id, sifra_predmeta, datum_upisa):
        enrollment_result = await self.db.execute(
            select(models.Enrollment).filter(models.Enrollment.student_id == student_id,
                                             models.Enrollment.sifra_predmeta == sifra_predmeta,
                                             models.Enrollment.datum_upisa == datum_upisa))
        enrollment = enrollment_result.scalars().first()
        try:
            await self.db.delete(enrollment)
            await self.db.commit()
            return { "Enrollment deleted" : True}
        except:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail='Database Error : delete enrollment failed')

