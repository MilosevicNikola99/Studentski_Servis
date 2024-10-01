from fastapi import Depends, HTTPException, status
from ..Repository.logging_repository import LoginRepository, get_logging_repository
from .utils import verify_password


def get_logging_service(repo: LoginRepository = Depends(get_logging_repository)):
    return LoginService(repo)

class LoginService:

    def __init__(self,repo : LoginRepository):
        self.repo = repo

    def authenticate_user(self,username,password):
        user = self.repo.get_user(username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        return user

