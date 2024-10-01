from fastapi import FastAPI ,Depends

from fastapi.security import OAuth2PasswordBearer

from .Routers import exams,students,courses,professors,enrollment,statistics,logging


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(exams.router)
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(professors.router)
app.include_router(enrollment.router)
app.include_router(statistics.router)
app.include_router(logging.router)



