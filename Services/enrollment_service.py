from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..Schemas import schemas
from ..Repository import enrollment_repository


def get_by_id(db: Session ,id: int):
    enrollments = enrollment_repository.get_enrolment_by_id(db,id)
    if enrollments is None:
        raise HTTPException(status_code = 404,detail = "Enrollments not found")

    return enrollments


def create_enrollment(db : Session,enrollment : schemas.EnrolmentCreate):
    if enrollment_repository.get_enrolment(db,enrollment.student_id,enrollment.sifra_predmeta,enrollment.datum_upisa):
        raise HTTPException(status_code=400,detail = "Enrollment already exists")
    return enrollment_repository.create_enrollment(db,enrollment)


def update_enrollment(db : Session ,student_id, sifra_predmeta, datum_upisa, up_enrollment):
    enrollment  = enrollment_repository.get_enrolment(db,student_id,sifra_predmeta,datum_upisa)
    if enrollment is None:
        raise HTTPException(status_code=400,detail = "Enrollment doesn't exists")
    return enrollment_repository.update_enrollment(db,enrollment,up_enrollment)


def delete_enrollment(db, student_id, sifra_predmeta, datum_upisa):
    enrollment = enrollment_repository.get_enrolment(db, student_id, sifra_predmeta, datum_upisa)
    if enrollment is None:
        raise HTTPException(status_code=400, detail="Enrollment doesn't exists")
    return enrollment_repository.delete_enrollment(db, enrollment)