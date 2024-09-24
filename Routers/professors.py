from fastapi import Depends, APIRouter

from ..Services.professor_services import ProfessorService, get_professor_service
from ..Database import  models , database
from ..Schemas import schemas

models.Base.metadata.create_all(bind=database.engine)

router = APIRouter(prefix="/professors", tags=["Professors"])

@router.post("/")
def create_professor(professor: schemas.ProfessorCreate ,professor_service : ProfessorService = Depends(get_professor_service)):
    return professor_service.create(professor)

@router.get("/{professor_id}")
def get_professor(professor_id: int, professor_service : ProfessorService = Depends(get_professor_service)):
    return professor_service.get_by_id(professor_id)

@router.put("/{professor_id}")
def update_professor(professor_id : int ,professor : schemas.ProfessorBase ,professor_service : ProfessorService = Depends(get_professor_service) ):
    return professor_service.update( schemas.Professor(**professor.model_dump() ,id=professor_id))

@router.delete("/{professor_id}")
def delete_professor(professor_id : int,professor_service : ProfessorService = Depends(get_professor_service)):
    return professor_service.delete(professor_id)