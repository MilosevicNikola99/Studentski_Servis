from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.testing.plugin.plugin_base import logging

from ..Repository.professor_repository import ProfessorRepository, get_professor_repository
from ..Schemas import schemas
from ..Services import permissions

def get_professor_service(repo : ProfessorRepository = Depends(get_professor_repository)):
    return ProfessorService(repo)

class ProfessorService:

    def __init__(self, professor_repository : ProfessorRepository ):
        self.professor_repository = professor_repository

    async def create(self, professor : schemas.ProfessorCreate,username : str):
        is_admin =  await permissions.is_admin(username,self.professor_repository.db)
        if not is_admin:
            raise HTTPException(status_code=403, detail="You are not authorized to create professor")

        if await self.professor_repository.get_professor(schemas.ProfessorBase(**professor.model_dump())):
            raise HTTPException(status_code=400,detail="Professor already exists")
        return await self.professor_repository.create_professor(professor)


    async def get_by_id(self, professor_id):
        professor = await self.professor_repository.get_professor_by_id(professor_id)
        if professor is None:
            raise HTTPException(status_code=404,detail="Professor not found")
        return professor

    async def get_professors(self, departman : str):
        if departman:
            professors = await self.professor_repository.get_professors_by_departmen(departman)
            if professors is None:
                raise HTTPException(status_code=404,detail="Professor not found")
            return professors
        return await self.professor_repository.get_all_professors()

    async def update(self, professor : schemas.ProfessorBase,professor_id : int,username : str):

        is_admin = await permissions.is_admin(username,self.professor_repository.db)
        if not is_admin:
            raise HTTPException(status_code=403, detail="You are not authorized to create professor")

        professor = await self.professor_repository.update_professor(professor,professor_id)
        if professor is None:
            raise HTTPException(status_code=404,detail="Professor not found")
        return professor


    async def delete(self, professor_id,username : str):
        is_admin = await  permissions.is_admin(username,self.professor_repository.db)
        if not is_admin:
            raise HTTPException(status_code=403, detail="You are not authorized to create professor")
        response = await self.professor_repository.delete_professor(professor_id)
        if response is None:
            raise HTTPException(status_code=404,detail="Professor not found")
        return response

