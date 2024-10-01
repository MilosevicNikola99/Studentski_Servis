from fastapi import HTTPException
from fastapi.params import Depends


from ..dependencies import get_db
from ..Database import models ,database
from ..Schemas import schemas

def get_professor_repository(db : database.SessionLocal = Depends(get_db)):
    return ProfessorRepository(db)

class ProfessorRepository:
    def __init__(self, db):
        self.db = db

    def get_professor(self,  professor : schemas.ProfessorBase):
        return self.db.query(models.Professor).filter(models.Professor.ime == professor.ime,
                                                 models.Professor.prezime == professor.prezime,
                                                 models.Professor.departman == professor.departman).first()


    def create_professor(self, professor : schemas.ProfessorCreate):
        db_professor = models.Professor(ime=professor.ime, prezime=professor.prezime,departman=professor.departman)
        try:
            self.db.add(db_professor)
            self.db.commit()
        except:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Database error")
        self.db.refresh(db_professor)
        return db_professor


    def get_professor_by_id(self, professor_id):
        return self.db.query(models.Professor).filter(models.Professor.id == professor_id).first()

    def get_professors_by_departmen(self, departman):
        return self.db.query(models.Professor).filter(models.Professor.departman == departman).all()

    def get_all_professors(self):
        return self.db.query(models.Professor).all()

    def update_professor(self, up_professor):
        professor = self.get_professor_by_id(up_professor.id)
        if professor:
            try:
                professor.ime = up_professor.ime
                professor.prezime = up_professor.prezime
                professor.departman = up_professor.departman
                self.db.commit()
            except:
                self.db.rollback()
                raise HTTPException(status_code=400, detail="Database error")
            self.db.refresh(professor)
            return professor
        return None


    def delete_professor(self, professor_id):
        professor = self.get_professor_by_id(professor_id)
        if professor:
            try:
                self.db.delete(professor)
                self.db.commit()
            except:
                self.db.rollback()
                raise HTTPException(status_code=400, detail="Database error")
            return {"Professor deleted" : True}
        return None

    def is_admin(self, username):
        admin = self.db.query(models.Admin).filter(username == models.Admin.username).first()
        if admin:
            return True
        return False


