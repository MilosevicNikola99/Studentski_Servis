from fastapi import HTTPException, Depends
from ..Repository.statistics_respository import StatisticsRepository,get_statistics_repository
from ..Services import permissions

def get_statistics_service(repo: StatisticsRepository = Depends(get_statistics_repository)):
    return StatisticsService(repo)

class StatisticsService:

    def __init__(self, repo: StatisticsRepository ):
        self.repo = repo

    async def get_sum_espb_for_student(self, student_id: int, username : str) -> int:
        if await permissions.check_permission(student_id, username,self.repo.db):
            espb = await self.repo.get_sum_espb_for_student(student_id)
            if espb is None:
                raise HTTPException(status_code=404, detail="Student not found")
            return espb
        else:
            raise HTTPException(status_code=401, detail="You are not authorized")

    async def count_passed_exams(self, student_id: int, username : str) -> int:
        if await permissions.check_permission(student_id, username,self.repo.db):
            passed_exams = await self.repo.count_passed_exams(student_id)
            if passed_exams is None:
                raise HTTPException(status_code=404, detail="Student not found")
            return passed_exams
        else:
            raise HTTPException(status_code=401, detail="You are not authorized")