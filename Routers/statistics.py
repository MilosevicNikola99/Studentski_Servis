from fastapi import Depends, APIRouter

from ..Services.statistic_service import StatisticsService, get_statistics_service
from ..Services.utils import verify_user


#models.Base.metadata.create_all(bind=database.engine)
router = APIRouter(prefix='/statistics', tags=['Statistics'])


@router.get("/{student_id}" )
async def statistics(student_id : int, statistics_service : StatisticsService = Depends(get_statistics_service),user_data = Depends(verify_user)):
    espb = await statistics_service.get_sum_espb_for_student(student_id,user_data['sub'])
    count_exams = await statistics_service.count_passed_exams(student_id,user_data['sub'])
    return {"ESPB" : espb, "Polozio" :count_exams}




