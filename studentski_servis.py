from fastapi import FastAPI

from fastapi.security import OAuth2PasswordBearer
from .Database.database import init_db
from .Routers import students, logging, professors, exams,courses , enrollment, statistics



app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(exams.router)
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(professors.router)
app.include_router(enrollment.router)
app.include_router(statistics.router)
app.include_router(logging.router)

#app.add_event_handler("startup", init_db)

# @app.on_event("startup")
# async def startup():
#     await init_db()
