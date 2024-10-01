from datetime import datetime
from fastapi import HTTPException , Depends
from ..dependencies import get_db
from ..Database import models,database
from ..Schemas import schemas

def get_exam_repository(db: database.SessionLocal = Depends(get_db)):
    return ExamRepository(db)

class ExamRepository:

    def __init__(self,db):
        self.db = db

    def get_exam_by_sifra(self, sifra_predemta:str):
        return self.db.query(models.Exam).filter(sifra_predemta == models.Exam.sifra_predmeta).first()


    def get_exam(self, student_id : int, sifra_predmeta : str, datum : datetime):
        return self.db.query(models.Exam).filter(student_id == models.Exam.student_id,
                                            sifra_predmeta == models.Exam.sifra_predmeta,
                                            datum == models.Exam.datum).first()


    def create_exam(self, exam : schemas.ExamCreate):
        db_exam = models.Exam(**exam.model_dump())

        try:
            self.db.add(db_exam)
        except:
            self.db.rollback()
            raise HTTPException(status_code=400, detail='Database Error : create exam failed')

        self.db.commit()
        self.db.refresh(db_exam)
        return db_exam



    def delete_exam(self, student_id: int ,sifra_predmeta : str , datum : datetime):
        exam = self.get_exam(student_id,sifra_predmeta,datum)
        if exam:
            try:
                self.db.delete(exam)
            except:
                self.db.rollback()
                raise HTTPException(status_code=400, detail='Database Error : delete exam failed')
            self.db.commit()
            return {"Exam deleted" : True}
        return None


    def update_exam(self, up_exam : schemas.Exam):
        exam = self.get_exam(up_exam.student_id, up_exam.sifra_predmeta, up_exam.datum)
        if exam:
            try:
                exam.datum = up_exam.datum
                exam.ocena = up_exam.ocena
                exam.polozen = up_exam.polozen
            except:
                self.db.rollback()
                raise HTTPException(status_code=400, detail='Database Error : update exam failed')

            self.db.commit()
            self.db.refresh(exam)
            return exam
        return None

    def is_admin(self, username):
        admin = self.db.query(models.Admin).filter(username == models.Admin.username).first()
        if admin:
            return True
        return False

    def is_professor(self, username):
        professor = self.db.query(models.UserProfessor).filter(username == models.UserProfessor.username).first()
        if professor:
            return True
        return False