from fastapi import HTTPException, Depends


from ..Repository.enrollment_repository import EnrollmentRepository, get_enrollment_repository
from ..Schemas import schemas


def get_enrollment_service(repo: EnrollmentRepository = Depends(get_enrollment_repository)):
    return EnrollmentService(repo)

class EnrollmentService:

    def __init__(self, enrollment_repository : EnrollmentRepository):
        self.enrollment_repository = enrollment_repository

    def get_by_id(self,student_id: int):
        enrollments = self.enrollment_repository.get_enrollments_by_id(student_id)
        if enrollments is None:
            raise HTTPException(status_code = 404,detail = "Enrollments not found")

        return enrollments

    def get_enrollments(self, student_id, sifra_predmeta, datum_upisa):
        if student_id and sifra_predmeta and datum_upisa:
            return self.enrollment_repository.get_enrollment(student_id,sifra_predmeta,datum_upisa)
        if student_id and sifra_predmeta is None and datum_upisa is None :
            return self.enrollment_repository.get_enrollments_by_id(student_id)
        if student_id is None and sifra_predmeta and datum_upisa is None:
            return self.enrollment_repository.get_enrollments_by_sifra(sifra_predmeta)
        if student_id is None and sifra_predmeta is None and datum_upisa:
            return self.enrollment_repository.get_enrollments_by_datum_upisa(datum_upisa)
        return self.enrollment_repository.get_enrollments()

    def create_enrollment(self,enrollment : schemas.EnrolmentCreate,username : str):
        if self.enrollment_repository.is_admin(username) or self.enrollment_repository.is_student(username,enrollment.student_id) :
            if self.enrollment_repository.get_enrollment(enrollment.student_id,enrollment.sifra_predmeta,enrollment.datum_upisa):
                raise HTTPException(status_code=400,detail = "Enrollment already exists")
            return self.enrollment_repository.create_enrollment(enrollment)
        else:
            raise HTTPException(status_code=401,detail="You are not authorized to create enrollment")


    def update_enrollment(self ,student_id, sifra_predmeta, datum_upisa, up_enrollment, username : str):
        if self.enrollment_repository.is_admin(username):
            enrollment  = self.enrollment_repository.get_enrollment(student_id,sifra_predmeta,datum_upisa)
            if enrollment is None:
                raise HTTPException(status_code=400,detail = "Enrollment doesn't exists")
            return self.enrollment_repository.update_enrollment(enrollment,up_enrollment)
        else:
            raise HTTPException(status_code=401,detail="You are not authorized to update enrollment")

    def delete_enrollment(self, student_id, sifra_predmeta, datum_upisa,username : str):
        if self.enrollment_repository.is_admin(username):
            enrollment = self.enrollment_repository.get_enrollment( student_id, sifra_predmeta, datum_upisa)
            if enrollment is None:
                raise HTTPException(status_code=400, detail="Enrollment doesn't exists")
            return self.enrollment_repository.delete_enrollment( enrollment)
        else:
            raise HTTPException(status_code=401,detail="You are not authorized to delete enrollment")

    def get_enrollment(self, student_id, sifra_predmeta, datum_upisa):
        enrollment = self.enrollment_repository.get_enrollment( student_id, sifra_predmeta, datum_upisa)
        if enrollment is None:
            raise HTTPException(status_code=400, detail="Enrollment doesn't exists")
        return enrollment


