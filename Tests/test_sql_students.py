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
async def test_create_student():

    auth = client.post("/login/user",data={"grant_type" : "password","username": "admin", "password": "password"} )
    assert auth.status_code == 200
    access_token = auth.json().get("access_token")
    response = client.post(
        "/students/",
        json={
                "ime": "Petar",
                "prezime": "Petrovic",
                "indeks": "100-2023",
                "user_id" :2
            } ,
        headers= {"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["ime"] == "Petar"
    assert data["prezime"] == "Petrovic"
    assert data["indeks"] == "100-2023"
    assert "id" in data
    student_id = data["id"]

    response = client.get(f"/students/{student_id}" , headers= {"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["ime"] == "Petar"
    assert data["prezime"] == "Petrovic"
    assert data["indeks"] == "100-2023"
    assert data["id"] == student_id


@pytest.mark.asyncio
async def test_update_student():

    auth = client.post("/login/user",data={"grant_type" : "password","username": "admin", "password": "password"} )
    assert auth.status_code == 200
    access_token = auth.json().get("access_token")

    response = client.put("/students/1",
                          json={
                                "ime": "Luka",
                                "prezime": "Lukic",
                                "indeks": "100-2023",
                                },
                          headers={"Authorization": f"Bearer {access_token}"}
                          )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["ime"] == "Luka"
    assert data["prezime"] == "Lukic"
    assert data["indeks"] == "100-2023"
    assert data["id"] == 1

@pytest.mark.asyncio
async def test_delete_student():
    auth = client.post("/login/user",data={"grant_type" : "password","username": "admin", "password": "password"} )
    assert auth.status_code == 200
    access_token = auth.json().get("access_token")

    response = client.delete("/students/1", headers= {"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == {"Student deleted" : True}