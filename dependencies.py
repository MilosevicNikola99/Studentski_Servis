from sqlalchemy.ext.asyncio import AsyncSession
from .Database import  database

# def get_db():
#     db = database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


async def get_db() -> AsyncSession:
    async with database.SessionLocal() as db:
        yield db

