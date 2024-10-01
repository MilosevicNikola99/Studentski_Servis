from fastapi import Depends
from ..dependencies import get_db
from ..Database import database
from ..Database import models
from sqlalchemy  import select
from sqlalchemy import func , join
from sqlalchemy.sql import and_



def get_statistics_repository(db: database.SessionLocal = Depends(get_db)):
    return StatisticsRepository(db)

class StatisticsRepository:

    def __init__(self,db):
        self.db = db

    def get_sum_espb_for_student(self, student_id: int) -> int:
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

        result = self.db.execute(stmt).scalar()

        return result

    def count_passed_exams(self, student_id: int):
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

        result = self.db.execute(stmt).scalar()

        return result

    def check_permission(self, student_id, username):
        student = self.db.query(models.UserStudent).filter(username == models.UserStudent.username, student_id == models.UserStudent.student_id).first()
        if student:
            return True
        professor = self.db.query(models.UserProfessor).filter(username == models.UserProfessor.username).first()
        if professor:
            return True
        admin = self.db.query(models.Admin).filter(username == models.Admin.username).first()
        if admin:
            return True
        return False

