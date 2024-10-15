from fastapi import Depends, APIRouter

from ..Services.student_services import StudentService , get_student_service
from ..Schemas import schemas
from ..Services.utils import verify_user



router = APIRouter(prefix='/students', tags=['Students'])


@router.post("/",response_model=schemas.Student)
async def create_student(student: schemas.StudentCreate ,student_service : StudentService = Depends(get_student_service),user_data = Depends(verify_user)):
    return await student_service.create(student,user_data['sub'])

@router.get("/{student_id}",response_model=schemas.Student)
async def get_student_by_id(student_id:int,student_service : StudentService = Depends(get_student_service),user_data = Depends(verify_user)):
    return await student_service.get_by_id(student_id,user_data["sub"])

@router.put("/{student_id}",response_model=schemas.Student)
async def update_student(student_id : int, student: schemas.StudentBase,student_service : StudentService = Depends(get_student_service),user_data = Depends(verify_user)):
    return await student_service.update(schemas.Student(id = student_id,**student.model_dump()),user_data["sub"])

@router.delete("/{student_id}")
async def delete_student(student_id: int,student_service : StudentService = Depends(get_student_service),user_data = Depends(verify_user)):
    return await student_service.delete(student_id,user_data["sub"])