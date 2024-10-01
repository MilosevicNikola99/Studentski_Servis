from datetime import datetime
from fastapi import Depends , APIRouter

from ..Services.exam_services import ExamServices, get_exam_service
from ..Database import  models , database
from ..Schemas import schemas
from ..Routers.logging import oauth2_scheme
from ..Services.utils import verify_access_token

models.Base.metadata.create_all(bind=database.engine)

router = APIRouter(prefix="/exams",tags=["Exams"])

@router.post("/")
def create_exam(exam: schemas.ExamCreate, exam_service: ExamServices = Depends(get_exam_service),token : str = Depends(oauth2_scheme)):
    user_data = verify_access_token(token)
    return exam_service.create(exam,user_data['sub'])

@router.get("/{student_id}/{sifra_predmeta}/{datum}")
def get_exam(student_id:int, sifra_predmeta:str, datum :datetime, exam_service: ExamServices = Depends(get_exam_service),token : str = Depends(oauth2_scheme)):
    user_data = verify_access_token(token)
    return exam_service.get_exam(student_id,sifra_predmeta,datum,user_data['sub'])

@router.put("/{student_id}/{sifra_predmeta}/{datum}")
def update_exam(student_id:int, sifra_predmeta:str, datum :datetime, exam : schemas.ExamBase, exam_service: ExamServices = Depends(get_exam_service), token : str = Depends(oauth2_scheme)):
    user_data = verify_access_token(token)
    exam = exam.model_dump()
    return exam_service.update( schemas.Exam(student_id=student_id,sifra_predmeta=sifra_predmeta,datum = datum,ocena=exam["ocena"],polozen=exam["polozen"]),user_data['sub'])

@router.delete("/{student_id}/{sifra_predmeta}/{datum}")
def delete_exam(student_id:int , sifra_predmeta:str , datum :datetime, exam_service: ExamServices = Depends(get_exam_service),token : str = Depends(oauth2_scheme)):
    user_data = verify_access_token(token)
    return exam_service.delete(student_id, sifra_predmeta, datum, user_data['sub'])