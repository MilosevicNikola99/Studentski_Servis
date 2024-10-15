import pytest
from starlette.testclient import TestClient

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


from ..Database.database import Base
from ..studentski_servis import app
from ..dependencies import get_db


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_test_app.db"

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=async_engine , class_=AsyncSession)


#Base.metadata.create_all(bind=engine)

async def override_get_db() -> AsyncSession:
    async with TestingSessionLocal() as db:
        async with async_engine.begin() as conn:
            # Kreiranje svih tabela pre svakog testa
            await conn.run_sync(Base.metadata.create_all)
        yield db
        #async with async_engine.begin() as conn:
            # Brisanje tabela nakon svakog testa
            #await conn.run_sync(Base.metadata.drop_all)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.mark.asyncio
async def test_create_professor():
    auth = client.post("/login/user", data={"grant_type": "password", "username": "admin", "password": "password"})
    assert auth.status_code == 200
    access_token = auth.json().get("access_token")

    response = client.post(
                    '/professors/',
                        json = {
                                  "ime": "Miroslav",
                                  "prezime": "Maric",
                                  "departman": "Racunarstvo i informatika",
                                  "user_id" : 3
                               },
                        headers = {"Authorization": f"Bearer {access_token}"}
                )
    assert response.status_code == 200
    assert response.json() == {
                                  "id" : 2,
                                  "ime": "Miroslav",
                                  "prezime": "Maric",
                                  "departman": "Racunarstvo i informatika",
                                  "user_id" : 3
                               }

@pytest.mark.asyncio
async def test_get_professor():
    response = client.get('/professors/2')
    assert response.status_code == 200, response.text
    assert response.json() == {
                                  "id" : 2,
                                  "ime": "Miroslav",
                                  "prezime": "Maric",
                                  "departman": "Racunarstvo i informatika",
                                  "user_id" : 3
                               }


@pytest.mark.asyncio
async def test_update_professor():
    auth = client.post("/login/user", data={"grant_type": "password", "username": "admin", "password": "password"})
    assert auth.status_code == 200
    access_token = auth.json().get("access_token")

    response = client.put('/professors/2',
                          json = {
                                  "ime": "Filip",
                                  "prezime": "Maric",
                                  "departman": "Racunarstvo i informatika"},
                          headers= {"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    assert response.json() == {
                                "id" : 2,
                                "ime": "Filip",
                                "prezime": "Maric",
                                "departman": "Racunarstvo i informatika",
                                "user_id" : 3}

@pytest.mark.asyncio
async def test_delete_professor():
    auth = client.post("/login/user", data={"grant_type": "password", "username": "admin", "password": "password"})
    assert auth.status_code == 200
    access_token = auth.json().get("access_token")

    response = client.delete('/professors/2',
                             headers= {"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    assert response.json() == {"Professor deleted" : True}
