from fastapi import Depends, APIRouter

from ..Services.statistic_service import StatisticsService, get_statistics_service
from ..Database import   database , models
from ..Routers.logging import oauth2_scheme
from ..Services.utils import verify_access_token


models.Base.metadata.create_all(bind=database.engine)
router = APIRouter(prefix='/statistics', tags=['Statistics'])


@router.get("/{student_id}" )
async def statistics(student_id : int, statistics_service : StatisticsService = Depends(get_statistics_service),token = Depends(oauth2_scheme)):
    user_data = verify_access_token(token)
    espb = statistics_service.get_sum_espb_for_student(student_id,user_data['sub'])
    count_exams = statistics_service.count_passed_exams(student_id,user_data['sub'])
    return {"ESPB" : espb, "Polozio" :count_exams}




