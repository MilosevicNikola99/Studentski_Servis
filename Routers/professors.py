from fastapi import Depends, APIRouter
import logging
from ..Services.utils import verify_user
from ..Services.professor_services import ProfessorService, get_professor_service

from ..Schemas import schemas

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/professors", tags=["Professors"])

@router.post("/")
async def create_professor(professor: schemas.ProfessorCreate ,professor_service : ProfessorService = Depends(get_professor_service),user_data = Depends(verify_user)):
    return await professor_service.create(professor,user_data["sub"])

@router.get("/")
async def get_professors(departman : str | None = None, professor_service : ProfessorService = Depends(get_professor_service)):
    return await professor_service.get_professors(departman)

@router.get("/{professor_id}")
async def get_professor_by_id(professor_id: int, professor_service : ProfessorService = Depends(get_professor_service)):
    return await professor_service.get_by_id(professor_id)


@router.put("/{professor_id}")
async def update_professor(professor_id : int ,professor : schemas.ProfessorBase ,professor_service : ProfessorService = Depends(get_professor_service),user_data = Depends(verify_user) ):
    return await professor_service.update( schemas.ProfessorBase(**professor.model_dump()),professor_id,user_data["sub"])

@router.delete("/{professor_id}")
async def delete_professor(professor_id : int,professor_service : ProfessorService = Depends(get_professor_service),user_data = Depends(verify_user)):
    return await professor_service.delete(professor_id,user_data["sub"])