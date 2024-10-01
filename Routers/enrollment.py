from datetime import datetime

from fastapi import Depends ,APIRouter
from ..Services.enrollment_service import EnrollmentService, get_enrollment_service
from ..Schemas import schemas
from ..Routers.logging import oauth2_scheme
from ..Services.utils import verify_access_token

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.post("/", response_model=schemas.Enrollment)
async def create_enrollment( enrollment : schemas.EnrolmentCreate, enrollment_service : EnrollmentService = Depends(get_enrollment_service),token : str = Depends(oauth2_scheme)):
    user_data = verify_access_token(token)
    return enrollment_service.create_enrollment(enrollment, user_data['sub'])

@router.get("/")
async def get_enrollment(student_id: int | None = None ,sifra_predmeta : str | None = None, datum_upisa : datetime | None = None,enrollment_service : EnrollmentService = Depends(get_enrollment_service)):
    return enrollment_service.get_enrollments( student_id, sifra_predmeta, datum_upisa)

@router.put("/{student_id}/{sifra_predmeta}/{datum_upisa}")
async def update_enrollment(student_id : int, sifra_predmeta : str ,datum_upisa: datetime, enrollment : schemas.Enrollment , enrollment_service : EnrollmentService = Depends(get_enrollment_service),token : str = Depends(oauth2_scheme)):
    user_data = verify_access_token(token)
    return enrollment_service.update_enrollment(student_id,sifra_predmeta,datum_upisa , enrollment,user_data['sub'])

@router.delete("/{student_id}/{sifra_predmeta}/{datum_upisa}")
async def delete_enrollment(student_id : int, sifra_predmeta : str ,datum_upisa: datetime, enrollment_service : EnrollmentService = Depends(get_enrollment_service),token : str = Depends(oauth2_scheme)):
    user_data = verify_access_token(token)
    return enrollment_service.delete_enrollment(student_id,sifra_predmeta,datum_upisa,user_data['sub'])