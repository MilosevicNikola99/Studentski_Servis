from datetime import datetime
from fastapi import Depends , APIRouter

from ..Services.exam_services import ExamServices, get_exam_service
from ..Schemas import schemas
from ..Services.utils import verify_user

#models.Base.metadata.create_all(bind=database.engine)

router = APIRouter(prefix="/exams",tags=["Exams"])

@router.post("/")
async def create_exam(exam: schemas.ExamCreate, exam_service: ExamServices = Depends(get_exam_service),user_data = Depends(verify_user)):
    return await exam_service.create(exam,user_data['sub'])

@router.get("/{student_id}/{sifra_predmeta}/{datum}")
async def get_exam(student_id:int, sifra_predmeta:str, datum :datetime, exam_service: ExamServices = Depends(get_exam_service),user_data = Depends(verify_user)):
    return await exam_service.get_exam(student_id,sifra_predmeta,datum,user_data['sub'])

@router.put("/{student_id}/{sifra_predmeta}/{datum}")
async def update_exam(student_id:int, sifra_predmeta:str, datum :datetime, exam : schemas.ExamBase, exam_service: ExamServices = Depends(get_exam_service),user_data = Depends(verify_user)):
    exam = exam.model_dump()
    return await exam_service.update( sifra_predmeta,schemas.Exam(student_id=student_id,sifra_predmeta=sifra_predmeta,datum = datum,ocena=exam["ocena"],polozen=exam["polozen"]),user_data['sub'])

@router.delete("/{student_id}/{sifra_predmeta}/{datum}")
async def delete_exam(student_id:int , sifra_predmeta:str , datum :datetime, exam_service: ExamServices = Depends(get_exam_service),user_data = Depends(verify_user)):
    return await exam_service.delete(student_id, sifra_predmeta, datum, user_data['sub'])