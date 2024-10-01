from fastapi import HTTPException
from fastapi.params import Depends


from ..Repository.professor_repository import ProfessorRepository, get_professor_repository
from ..Schemas import schemas


def get_professor_service(repo : ProfessorRepository = Depends(get_professor_repository)):
    return ProfessorService(repo)

class ProfessorService:

    def __init__(self, professor_repository : ProfessorRepository ):
        self.professor_repository = professor_repository

    def create(self, professor : schemas.ProfessorCreate,username : str):
        is_admin = self.professor_repository.is_admin(username)
        if not is_admin:
            raise HTTPException(status_code=403, detail="You are not authorized to create professor")

        if self.professor_repository.get_professor(professor):
            raise HTTPException(status_code=400,detail="Professor already exists")
        return self.professor_repository.create_professor(professor)


    def get_by_id(self, professor_id):
        professor =  self.professor_repository.get_professor_by_id(professor_id)
        if professor is None:
            raise HTTPException(status_code=404,detail="Professor not found")
        return professor

    def get_professors(self, departman : str):
        if departman:
            professors = self.professor_repository.get_professors_by_departmen(departman)
            if professors is None:
                raise HTTPException(status_code=404,detail="Professor not found")
            return professors
        return self.professor_repository.get_all_professors()

    def update(self, professor : schemas.Professor,username : str):
        is_admin = self.professor_repository.is_admin(username)
        if not is_admin:
            raise HTTPException(status_code=403, detail="You are not authorized to create professor")

        professor = self.professor_repository.update_professor(professor)
        if professor is None:
            raise HTTPException(status_code=404,detail="Professor not found")
        return professor


    def delete(self, professor_id,username : str):
        is_admin = self.professor_repository.is_admin(username)
        if not is_admin:
            raise HTTPException(status_code=403, detail="You are not authorized to create professor")
        response = self.professor_repository.delete_professor(professor_id)
        if response is None:
            raise HTTPException(status_code=404,detail="Professor not found")
        return response

