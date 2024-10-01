from fastapi import Depends
from ..dependencies import get_db
from ..Database import database
from ..Database import models

def get_logging_repository(db: database.SessionLocal = Depends(get_db)):
    return LoginRepository(db)

class LoginRepository:

    def __init__(self,db):
        self.db = db

    def get_user(self,username : str):
        return self.db.query(models.User).filter(models.User.username == username).first()

