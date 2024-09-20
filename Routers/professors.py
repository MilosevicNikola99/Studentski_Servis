from fastapi import  Depends , APIRouter
from sqlalchemy.orm import Session


from ..Database import  models , database
from ..Schemas import schemas
from ..Services import  professor_services
from ..dependencies import get_db

models.Base.metadata.create_all(bind=database.engine)

router = APIRouter(prefix="/professors", tags=["professors"])

@router.post("/")
def create_professor(professor: schemas.ProfessorCreate , db : Session = Depends(get_db)):
    return professor_services.create(db, professor)

@router.get("/{id}")
def get_professor(id: int, db : Session = Depends(get_db)):
    return professor_services.get_by_id(db, id)

@router.put("/{id}")
def update_professor(id : int ,professor : schemas.ProfessorBase , db : Session = Depends(get_db)):
    return professor_services.update(db, schemas.Professor(**professor.model_dump() ,id=id))

@router.delete("/{id}")
def delete_professor(id : int, db : Session = Depends(get_db)):
    return professor_services.delete(db, id)