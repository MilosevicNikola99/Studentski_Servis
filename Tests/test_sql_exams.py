from starlette.testclient import TestClient
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..Database.database import Base
from ..studentski_servis import app
from ..dependencies import get_db

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_test_app.db"

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
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
async def test_create_exam():

    auth = client.post("/login/user",data={"grant_type" : "password","username": "admin", "password": "password"} )
    assert auth.status_code == 200
    access_token = auth.json().get("access_token")

    response = client.post("/exams/",
                            json={
                                      "datum": "2024-09-18 13:02:21.702000",
                                      "ocena": 6,
                                      "polozen": True,
                                      "student_id": 1,
                                      "sifra_predmeta": "P120"
                            } ,
                            headers= {"Authorization": f"Bearer {access_token}"}
                            )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["datum"] == "2024-09-18T13:02:21.702000"
    assert data["ocena"] == 6
    assert data["student_id"] == 1
    assert data["sifra_predmeta"] == "P120"


@pytest.mark.asyncio
async def test_get_exams():
    auth = client.post("/login/user",data={"grant_type" : "password","username": "admin", "password": "password"} )
    assert auth.status_code == 200
    access_token = auth.json().get("access_token")

    response = client.get("/exams/1/P120/2024-09-18T13:02:21.702000",headers= {"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["datum"] == "2024-09-18T13:02:21.702000"
    assert data["ocena"] == 6
    assert data["student_id"] == 1
    assert data["sifra_predmeta"] == "P120"

@pytest.mark.asyncio
async def test_update_exams():
    auth = client.post("/login/user", data={"grant_type": "password", "username": "admin", "password": "password"})
    assert auth.status_code == 200
    access_token = auth.json().get("access_token")

    response = client.put("/exams/1/P120/2024-09-18 13:02:21.702000",
                          json= {
                              "datum": "2024-09-18T13:02:21.702000",
                              "ocena": 9,
                              "polozen": True
                          },
                          headers= {"Authorization": f"Bearer {access_token}"}
                          )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["ocena"] == 9
    assert data["polozen"] == True

@pytest.mark.asyncio
async def test_delete_exams():
    auth = client.post("/login/user", data={"grant_type": "password", "username": "admin", "password": "password"})
    assert auth.status_code == 200
    access_token = auth.json().get("access_token")

    response = client.delete("/exams/1/P120/2024-09-18T13:02:21.702000", headers= {"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == {"Exam deleted" : True}