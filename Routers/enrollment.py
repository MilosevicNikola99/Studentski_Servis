from datetime import datetime
import logging
from fastapi import Depends ,APIRouter
from ..Services.enrollment_service import EnrollmentService, get_enrollment_service
from ..Schemas import schemas
from ..Services.utils import verify_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.post("/", response_model=schemas.Enrollment)
async def create_enrollment( enrollment : schemas.EnrolmentCreate,
                             enrollment_service : EnrollmentService = Depends(get_enrollment_service),
                             user_data = Depends(verify_user)):
    return await enrollment_service.create_enrollment(enrollment, user_data['sub'])

@router.get("/")
async def get_enrollment(student_id: int | None = None ,
                         sifra_predmeta : str | None = None,
                         datum_upisa : datetime | None = None,
                         enrollment_service : EnrollmentService = Depends(get_enrollment_service)):
    return await enrollment_service.get_enrollments( student_id, sifra_predmeta, datum_upisa)

@router.put("/{student_id}/{sifra_predmeta}/{datum_upisa}")
async def update_enrollment(student_id : int, sifra_predmeta : str ,
                            datum_upisa: datetime,
                            enrollment : schemas.Enrollment ,
                            enrollment_service : EnrollmentService = Depends(get_enrollment_service),
                            user_data = Depends(verify_user)):
    return await enrollment_service.update_enrollment(student_id,sifra_predmeta,datum_upisa , enrollment,user_data['sub'])

@router.delete("/{student_id}/{sifra_predmeta}/{datum_upisa}")
async def delete_enrollment(student_id : int, sifra_predmeta : str ,
                            datum_upisa: datetime,
                            enrollment_service : EnrollmentService = Depends(get_enrollment_service),
                            user_data = Depends(verify_user)):
    return await enrollment_service.delete_enrollment(student_id,sifra_predmeta,datum_upisa,user_data['sub'])