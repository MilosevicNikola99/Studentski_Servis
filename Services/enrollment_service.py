from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..Schemas import schemas
from ..Repository import enrollment_repository


def get_by_id(db: Session ,id: int):
    enrollments = enrollment_repository.get_enrollments_by_id(db,id)
    if enrollments is None:
        raise HTTPException(status_code = 404,detail = "Enrollments not found")

    return enrollments

def get_enrollments(db, student_id, sifra_predmeta, datum_upisa):
    if student_id and sifra_predmeta and datum_upisa:
        return enrollment_repository.get_enrollment(db,student_id,sifra_predmeta,datum_upisa)
    if student_id and sifra_predmeta is None and datum_upisa is None :
        return enrollment_repository.get_enrollments_by_id(db,student_id)
    if student_id is None and sifra_predmeta and datum_upisa is None:
        return enrollment_repository.get_enrollments_by_sifra(db,sifra_predmeta)
    if student_id is None and sifra_predmeta is None and datum_upisa:
        return enrollment_repository.get_enrollments_by_datum_upisa(db,datum_upisa)
    return enrollment_repository.get_enrollments(db)

def create_enrollment(db : Session,enrollment : schemas.EnrolmentCreate):
    if enrollment_repository.get_enrollment(db,enrollment.student_id,enrollment.sifra_predmeta,enrollment.datum_upisa):
        raise HTTPException(status_code=400,detail = "Enrollment already exists")
    return enrollment_repository.create_enrollment(db,enrollment)


def update_enrollment(db : Session ,student_id, sifra_predmeta, datum_upisa, up_enrollment):
    enrollment  = enrollment_repository.get_enrollment(db,student_id,sifra_predmeta,datum_upisa)
    if enrollment is None:
        raise HTTPException(status_code=400,detail = "Enrollment doesn't exists")
    return enrollment_repository.update_enrollment(db,enrollment,up_enrollment)


def delete_enrollment(db, student_id, sifra_predmeta, datum_upisa):
    enrollment = enrollment_repository.get_enrollment(db, student_id, sifra_predmeta, datum_upisa)
    if enrollment is None:
        raise HTTPException(status_code=400, detail="Enrollment doesn't exists")
    return enrollment_repository.delete_enrollment(db, enrollment)


def get_enrollment(db, student_id, sifra_predmeta, datum_upisa):
    enrollment = enrollment_repository.get_enrollment(db, student_id, sifra_predmeta, datum_upisa)
    if enrollment is None:
        raise HTTPException(status_code=400, detail="Enrollment doesn't exists")
    return enrollment


