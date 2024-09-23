from datetime import datetime
from fastapi import Depends ,APIRouter
from ..Services.enrollment_service import EnrollmentService, get_enrollment_service
from ..Schemas import schemas


router = APIRouter(prefix="/enrollments", tags=["enrollments"])

@router.post("/", response_model=schemas.Enrollment)
async def create_enrollment( enrollment : schemas.EnrolmentCreate, enrollment_service : EnrollmentService = Depends(get_enrollment_service)):
    return enrollment_service.create_enrollment(enrollment)

@router.get("/")
async def get_enrollment(student_id: int | None = None ,sifra_predmeta : str | None = None, datum_upisa : datetime | None = None,enrollment_service : EnrollmentService = Depends(get_enrollment_service)):
    return enrollment_service.get_enrollments( student_id, sifra_predmeta, datum_upisa)

@router.put("/{student_id}/{sifra_predemta}/{datum_upisa}")
async def update_enrollment(student_id : int, sifra_predmeta : str ,datum_upisa: datetime, enrollment : schemas.Enrollment , enrollment_service : EnrollmentService = Depends(get_enrollment_service)):
    return enrollment_service.update_enrollment(student_id,sifra_predmeta,datum_upisa , enrollment)

@router.delete("/{student_id}/{sifra_predemta}/{datum_upisa}")
async def delete_enrollment(student_id : int, sifra_predmeta : str ,datum_upisa: datetime, enrollment_service : EnrollmentService = Depends(get_enrollment_service)):
    return enrollment_service.delete_enrollment(student_id,sifra_predmeta,datum_upisa)