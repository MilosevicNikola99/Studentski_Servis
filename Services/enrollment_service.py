from fastapi import HTTPException, Depends


from ..Repository.enrollment_repository import EnrollmentRepository, get_enrollment_repository
from ..Schemas import schemas
from ..Services import permissions

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_enrollment_service(repo: EnrollmentRepository = Depends(get_enrollment_repository)):
    return EnrollmentService(repo)

class EnrollmentService:

    def __init__(self, enrollment_repository : EnrollmentRepository):
        self.enrollment_repository = enrollment_repository

    async def get_by_id(self,student_id: int):
        enrollments = await self.enrollment_repository.get_enrollments_by_id(student_id)
        if enrollments is None:
            raise HTTPException(status_code = 404,detail = "Enrollments not found")
        return enrollments

    async def get_enrollments(self, student_id, sifra_predmeta, datum_upisa):

        if student_id and sifra_predmeta and datum_upisa:
            return await self.enrollment_repository.get_enrollment(student_id,sifra_predmeta,datum_upisa)
        if student_id and sifra_predmeta is None and datum_upisa is None :
            return await self.enrollment_repository.get_enrollments_by_id(student_id)
        if student_id is None and sifra_predmeta and datum_upisa is None:
            return await self.enrollment_repository.get_enrollments_by_sifra(sifra_predmeta)
        if student_id is None and sifra_predmeta is None and datum_upisa:
            return await self.enrollment_repository.get_enrollments_by_datum_upisa(datum_upisa)
        return await self.enrollment_repository.get_enrollments()

    async def create_enrollment(self,enrollment : schemas.EnrolmentCreate,username : str):
        enrollment.datum_upisa = enrollment.datum_upisa.replace(tzinfo=None)
        if await permissions.is_admin(username,self.enrollment_repository.db) or await permissions.is_student(username,enrollment.student_id,self.enrollment_repository.db) :
            if await self.enrollment_repository.get_enrollment(enrollment.student_id,enrollment.sifra_predmeta,enrollment.datum_upisa):
                raise HTTPException(status_code=400,detail = "Enrollment already exists")
            return await self.enrollment_repository.create_enrollment(enrollment)
        else:
            raise HTTPException(status_code=401,detail="You are not authorized to create enrollment")


    async def update_enrollment(self ,student_id, sifra_predmeta, datum_upisa, up_enrollment, username : str):
        if await permissions.is_admin(username,self.enrollment_repository.db):
            enrollment  = await self.enrollment_repository.get_enrollment(student_id,sifra_predmeta,datum_upisa)
            if enrollment is None:
                raise HTTPException(status_code=400,detail = "Enrollment doesn't exists")
            return await self.enrollment_repository.update_enrollment(student_id,sifra_predmeta,datum_upisa,up_enrollment)
        else:
            raise HTTPException(status_code=401,detail="You are not authorized to update enrollment")

    async def delete_enrollment(self, student_id, sifra_predmeta, datum_upisa,username : str):
        if await permissions.is_admin(username,self.enrollment_repository.db):
            enrollment = await self.enrollment_repository.get_enrollment( student_id, sifra_predmeta, datum_upisa)
            if enrollment is None:
                raise HTTPException(status_code=400, detail="Enrollment doesn't exists")
            return await self.enrollment_repository.delete_enrollment( student_id,sifra_predmeta,datum_upisa)
        else:
            raise HTTPException(status_code=401,detail="You are not authorized to delete enrollment")

    async def get_enrollment(self, student_id, sifra_predmeta, datum_upisa):
        enrollment = await self.enrollment_repository.get_enrollment( student_id, sifra_predmeta, datum_upisa)
        if enrollment is None:
            raise HTTPException(status_code=400, detail="Enrollment doesn't exists")
        return enrollment


