from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker ,declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = ("postgresql+asyncpg://postgres:postgres@localhost/studentski_servis")


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
