from fastapi import Depends
from sqlalchemy import select

from ..dependencies import get_db
from ..Database import database
from ..Database import models

def get_logging_repository(db: database.SessionLocal = Depends(get_db)):
    return LoginRepository(db)

class LoginRepository:

    def __init__(self,db):
        self.db = db

    async def get_user(self,username : str):
        stmt = select(models.User).filter(models.User.username == username)
        result =await self.db.execute(stmt)
        return result.scalar_one_or_none()

