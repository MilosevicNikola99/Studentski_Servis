from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session


from Database import  models , database
from Schemas import schemas
from Services import  course_services


models.Base.metadata.create_all(bind=database.engine)

router = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/courses/")
def create_course(course: schemas.Course , db : Session = Depends(get_db)):
    return course_services.create(db, course)

@router.get("/courses/{sifra_predmeta}")
def get_course(sifra_predmeta, db : Session = Depends(get_db)):
    return course_services.get_by_sifra(db, sifra_predmeta)

@router.put("/courses/{sifra_predmeta}")
def update_course(sifra_predmeta,course : schemas.CourseBase , db : Session = Depends(get_db)):
    return course_services.update(db, schemas.Course(**course.model_dump() ,sifra_predmeta=sifra_predmeta))

@router.delete("/courses/{sifra_predmeta}")
def delete_course(sifra_predmeta : str, db : Session = Depends(get_db)):
    return course_services.delete(db, sifra_predmeta)