from fastapi import  Depends , APIRouter
from ..Database import  models , database
from ..Schemas import schemas
from ..Services.course_services import  CourseServices, get_course_service
from ..Services.utils import verify_user


#models.Base.metadata.create_all(bind=database.engine)

router = APIRouter(prefix='/courses',tags=['Courses'])

@router.post("/",response_model=schemas.Course)
async def create_course(course: schemas.CourseCreate ,course_services : CourseServices = Depends(get_course_service),user_data = Depends(verify_user)):
    return await course_services.create(course,user_data["sub"])

@router.get("/")
async def get_courses(profesor_id : int | None = None, naziv : str | None = None, departman : str | None = None,course_services : CourseServices = Depends(get_course_service)):
    return await course_services.get_courses(profesor_id,naziv,departman)

@router.get("/{sifra_predmeta}",response_model=schemas.Course)
async def get_course(sifra_predmeta, course_services : CourseServices = Depends(get_course_service)):
    return await course_services.get_by_sifra( sifra_predmeta)

@router.put("/{sifra_predmeta}")
async def update_course(sifra_predmeta,course : schemas.CourseBase ,course_services : CourseServices = Depends(get_course_service),user_data = Depends(verify_user)):
    return await course_services.update( schemas.CourseBase(**course.model_dump()),sifra_predmeta,user_data["sub"])

@router.delete("/{sifra_predmeta}")
async def delete_course(sifra_predmeta : str,course_services : CourseServices = Depends(get_course_service),user_data = Depends(verify_user)):
    return await course_services.delete( sifra_predmeta,user_data["sub"])