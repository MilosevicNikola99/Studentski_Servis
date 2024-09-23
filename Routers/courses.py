from fastapi import  Depends , APIRouter
from ..Database import  models , database
from ..Schemas import schemas
from ..Services.course_services import  CourseServices, get_course_service


models.Base.metadata.create_all(bind=database.engine)

router = APIRouter(prefix='/courses',tags=['courses'])

@router.post("/")
def create_course(course: schemas.Course ,course_services : CourseServices = Depends(get_course_service)):
    return course_services.create( course)

@router.get("/{sifra_predmeta}")
def get_course(sifra_predmeta, course_services : CourseServices = Depends(get_course_service)):
    return course_services.get_by_sifra( sifra_predmeta)

@router.put("/{sifra_predmeta}")
def update_course(sifra_predmeta,course : schemas.CourseBase ,course_services : CourseServices = Depends(get_course_service)):
    return course_services.update( schemas.Course(**course.model_dump() ,sifra_predmeta=sifra_predmeta))

@router.delete("/{sifra_predmeta}")
def delete_course(sifra_predmeta : str,course_services : CourseServices = Depends(get_course_service) ):
    return course_services.delete( sifra_predmeta)