from datetime import datetime

from fastapi import Depends, FastAPI ,APIRouter
from sqlalchemy.cyextension.processors import date_cls
from sqlalchemy.orm import Session

from ..Database import  models , database
from ..Schemas import schemas
from ..Services import enrollment_service
from ..dependencies import get_db
router = APIRouter(prefix="/enrollments", tags=["enrollments"])

@router.post("/", response_model=schemas.Enrollment)
async def enrollment(enrollment: schemas.EnrolmentCreate,  db : Session = Depends(get_db)):
    return enrollment_service.create_enrollment(db,enrollment)

@router.get("/{student_id}")
async def get_enrollment(student_id: int , db : Session = Depends(get_db)):
    return enrollment_service.get_by_id(db,student_id)

@router.put("/{student_id}/{sifra_predemta}/{datum_upisa}")
async def update_enrollment(student_id : int, sifra_predmeta : str ,datum_upisa: datetime, enrollment : schemas.Enrollment , db : Session = Depends(get_db)):
    return enrollment_service.update_enrollment(db,student_id,sifra_predmeta,datum_upisa , enrollment)

@router.delete("/{student_id}/{sifra_predemta}/{datum_upisa}")
async def delete_enrollment(student_id : int, sifra_predmeta : str ,datum_upisa: datetime, db : Session = Depends(get_db)):
    return enrollment_service.delete_enrollment(db,student_id,sifra_predmeta,datum_upisa)