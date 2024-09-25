from fastapi import  Depends , APIRouter
from ..Database import  models , database
from ..Schemas import schemas
from ..Services.course_services import  CourseServices, get_course_service


models.Base.metadata.create_all(bind=database.engine)

router = APIRouter(prefix='/courses',tags=['Courses'])

@router.post("/",response_model=schemas.Course)
def create_course(course: schemas.CourseCreate ,course_services : CourseServices = Depends(get_course_service)):
    return course_services.create(course)

@router.get("/")
def get_courses(profesor_id : int | None = None, naziv : str | None = None, departman : str | None = None,course_services : CourseServices = Depends(get_course_service)):
    return course_services.get_courses(profesor_id,naziv,departman)

@router.get("/{sifra_predmeta}",response_model=schemas.Course)
def get_course(sifra_predmeta, course_services : CourseServices = Depends(get_course_service)):
    return course_services.get_by_sifra( sifra_predmeta)

@router.put("/{sifra_predmeta}")
def update_course(sifra_predmeta,course : schemas.CourseBase ,course_services : CourseServices = Depends(get_course_service)):
    return course_services.update( schemas.CourseCreate(**course.model_dump() ,sifra_predmeta=sifra_predmeta))

@router.delete("/{sifra_predmeta}")
def delete_course(sifra_predmeta : str,course_services : CourseServices = Depends(get_course_service) ):
    return course_services.delete( sifra_predmeta)