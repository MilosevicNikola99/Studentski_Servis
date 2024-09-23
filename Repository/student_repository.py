from fastapi import HTTPException
from fastapi import Depends
from ..dependencies import get_db
from ..Database import database
from ..Database import models
from ..Schemas import schemas

def get_student_repository(db: database.SessionLocal = Depends(get_db)):
    return StudentRepository(db)

class StudentRepository:

    def __init__(self,db):
        self.db = db

    def create_student(self,student : schemas.StudentCreate):
        db_student = models.Student(ime=student.ime,prezime=student.prezime,indeks=student.indeks)
        try:
            self.db.add(db_student)
            self.db.commit()
        except:
            self.db.rollback()
            raise HTTPException(status_code=400, detail='Database Error : create student failed')

        self.db.refresh(db_student)
        return db_student

    def get_student_by_id(self, student_id : int):
        return self.db.query(models.Student).filter(student_id == models.Student.id).first()


    def get_student_by_indeks(self, indeks : str):
        return self.db.query(models.Student).filter(indeks == models.Student.indeks).first()

    def update_student(self,up_student : schemas.Student):
        student = self.db.query(models.Student).filter(up_student.id == models.Student.id).first()
        if student:
            try:
                student.ime = up_student.ime
                student.prezime = up_student.prezime
                student.indeks = up_student.indeks
                self.db.commit()
            except:
                self.db.rollback()
                raise HTTPException(status_code=400, detail='Database Error : update student failed')

            self.db.refresh(student)
            return student
        return None


    def delete_student(self, student_id : int):
        student = self.db.query(models.Student).filter(student_id == models.Student.id).first()
        if student:
            try:
                self.db.delete(student)
                self.db.commit()
            except:
                self.db.rollback()
                raise HTTPException(status_code=400, detail='Database Error : delete student failed')
            self.db.commit()
            return {"Student deleted" : True}
        return None