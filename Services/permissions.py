import logging
from ..Database import models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def check_permission(student_id : int, username : str, db: AsyncSession ):

    logger.info("Checking permissions for user: %s and student_id: %d", username, student_id)

    student_result = await db.execute(
        select(models.Student, models.User)
        .join(models.User, models.User.id == models.Student.user_id)
        .filter(models.User.username == username, models.Student.id == student_id)
    )
    student_record = student_result.fetchone()

    if student_record is not None:
        user, student = student_record
        logger.info("Student record: %s %s", user, student)
        return True

    professor_result = await db.execute(
        select(models.User).filter(models.User.username == username, models.User.role == "professor")
    )
    professor = professor_result.scalars().first()
    if professor:
        return True

    if await is_admin(username,db):
        return True

    return False

async def is_admin(username : str ,db :  AsyncSession):
    admin_result = await db.execute(
        select(models.User).filter(models.User.username == username, models.User.role == "admin")
    )
    admin = admin_result.scalars().first()
    if admin:
        return True
    else:
        return False

async def is_professor(username : str,sifra_predmeta : str,db : AsyncSession):

    result = await db.execute(
        select(models.User)
        .join(models.Professor,models.User.id == models.Professor.user_id)
        .join(models.Course,models.Course.profesor_id == models.Professor.id)
        .join(models.Exam,models.Exam.sifra_predmeta == models.Course.sifra_predmeta)
        .where( models.Exam.sifra_predmeta == sifra_predmeta,
                            models.User.username == username
                )
    )
    professor = result.scalars().first()
    if professor:
        return True
    return False

async def is_student( username : str, student_id : int,db : AsyncSession):
    student_result = await db.execute(
        select(models.Student, models.User)
        .join(models.User, models.User.id == models.Student.user_id)
        .filter(models.User.username == username, models.Student.id == student_id)
    )
    student_record = student_result.fetchone()

    if student_record is not None:
        return True
    else:
        return False
