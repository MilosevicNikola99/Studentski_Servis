from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_db
from ..Database import models
from ..Schemas import schemas

def get_professor_repository(db : AsyncSession = Depends(get_db)):
    return ProfessorRepository(db)

class ProfessorRepository:
    def __init__(self, db : AsyncSession):
        self.db = db

    async def get_professor(self,  professor : schemas.ProfessorBase):
        professor = await self.db.execute(select(models.Professor).where(models.Professor.ime == professor.ime,
                                                 models.Professor.prezime == professor.prezime,
                                                 models.Professor.departman == professor.departman))

        return professor.scalar_one_or_none()


    async def create_professor(self, professor : schemas.ProfessorCreate):
        db_professor = models.Professor(ime=professor.ime, prezime=professor.prezime,departman=professor.departman,user_id=professor.user_id)
        try:
            self.db.add(db_professor)
            await self.db.commit()
        except:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Database error")
        await self.db.refresh(db_professor)
        return db_professor


    async def get_professor_by_id(self, professor_id):
        professor = await self.db.execute(select(models.Professor).filter(models.Professor.id == professor_id))
        return professor.scalar_one_or_none()

    async def get_professors_by_departmen(self, departman):
        result =await self.db.execute(select(models.Professor).filter(models.Professor.departman == departman))
        professors = result.scalars().all()
        return professors

    async def get_all_professors(self):
        result = await self.db.execute(select(models.Professor))
        professors = result.scalars().all()
        return professors

    async def update_professor(self, up_professor,professor_id):
        professor = await self.get_professor_by_id(professor_id)
        if professor:
            try:
                professor.ime = up_professor.ime
                professor.prezime = up_professor.prezime
                professor.departman = up_professor.departman
                await self.db.commit()
            except:
                await self.db.rollback()
                raise HTTPException(status_code=400, detail="Database error")
            await self.db.refresh(professor)
            return professor
        return None


    async def delete_professor(self, professor_id):
        professor = await self.get_professor_by_id(professor_id)
        if professor:
            try:
                await self.db.delete(professor)
                await self.db.commit()
            except:
                await self.db.rollback()
                raise HTTPException(status_code=400, detail="Database error")
            return {"Professor deleted" : True}
        return None


