from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from ..Services.logging_services import LoginService, get_logging_service
from ..Services.utils import create_access_token


router = APIRouter(prefix="/login")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/user")

@router.post("/user")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(),login_service : LoginService = Depends(get_logging_service)):
    user = await login_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token(data={"id": user.id, "sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

