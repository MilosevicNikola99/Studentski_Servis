from fastapi import FastAPI ,Depends
from sqlalchemy  import select
from sqlalchemy.orm import Session
from sqlalchemy import func , join
from sqlalchemy.sql import and_
from .Routers import exams,students,courses

from .Database import  models
from .dependencies import get_db

app = FastAPI()



def get_sum_espb_for_student(db: Session, student_id: int) -> int:
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

    result = db.execute(stmt).scalar()

    return result or 0

def count_passed_exams(db: Session, student_id: int):
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

    result = db.execute(stmt).scalar()

    return result or 0
app.include_router(exams.router)
app.include_router(students.router)
app.include_router(courses.router)

@app.get("/statistics/{student_id}")
async def statistics(student_id : int , db : Session = Depends(get_db)):
    espb = get_sum_espb_for_student(db,student_id)
    count_exams = count_passed_exams(db,student_id)
    return { "ESPB" : espb, "Polozio" :count_exams }

