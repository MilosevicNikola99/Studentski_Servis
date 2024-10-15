from starlette.testclient import TestClient

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import pytest
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
async def test_statistics():
    auth = client.post("/login/user",data={"grant_type" : "password","username": "admin", "password": "password"} )
    assert auth.status_code == 200
    access_token = auth.json().get("access_token")
    response = client.post("/students/",
                    json={
                        "ime": "Petar",
                        "prezime": "Petrovic",
                        "indeks": "100-2023",
                        "user_id" :2
                    },headers= {"Authorization": f"Bearer {access_token}"}
    )
    data = response.json()
    assert "id" in data
    student_id = data["id"]

    client.post("/courses/",
                json={
                        "naziv": "Programiranje1",
                        "espb": 6,
                        "sifra_predmeta": "P120",
                        "profesor_id" : 1
                },
                headers= {"Authorization": f"Bearer {access_token}"})

    client.post("/courses/",
                json={
                    "naziv": "Programiranje2",
                    "espb": 6,
                    "sifra_predmeta": "P121",
                    "profesor_id": 1
                },
                headers= {"Authorization": f"Bearer {access_token}"}
                )

    client.post("/courses/",
                json={
                    "naziv": "Analiza1",
                    "espb": 6,
                    "sifra_predmeta": "M101",
                    "profesor_id": 1
                },
                headers= {"Authorization": f"Bearer {access_token}"})

    client.post("/courses/",
                json={
                    "naziv": "Analiza2",
                    "espb": 6,
                    "sifra_predmeta": "M102",
                    "profesor_id": 1
                },
                headers= {"Authorization": f"Bearer {access_token}"})
    client.post("/exams/" ,
                json={
                    "datum": "2024-09-19T07:38:46.871Z",
                    "ocena": 7,
                    "polozen": True,
                    "student_id": student_id,
                    "sifra_predmeta": "P120"
                },
                headers= {"Authorization": f"Bearer {access_token}"})
    client.post("/exams/" ,
                json={
                    "datum": "2024-09-19T07:38:46.871Z",
                    "ocena": 5,
                    "polozen": False,
                    "student_id": student_id,
                    "sifra_predmeta": "P121"
                },
                headers= {"Authorization": f"Bearer {access_token}"})
    client.post("/exams/" ,
                json={
                    "datum": "2024-09-19T07:38:46.871Z",
                    "ocena": 8,
                    "polozen": True,
                    "student_id": student_id,
                    "sifra_predmeta": "M101"
                },
                headers= {"Authorization": f"Bearer {access_token}"})
    client.post("/exams/" ,
                json={
                    "datum": "2024-09-19T07:38:46.871Z",
                    "ocena": 5,
                    "polozen": False,
                    "student_id": student_id,
                    "sifra_predmeta": "M102"
                },
                headers= {"Authorization": f"Bearer {access_token}"})

    respone = client.get(f"/statistics/{student_id}/",headers= {"Authorization": f"Bearer {access_token}"})
    assert respone.status_code == 200
    assert respone.json() == {"ESPB" : 12, "Polozio" :2}


    client.delete(f"/exams/{student_id}/P120/2024-09-19T07:38:46.871Z",headers= {"Authorization": f"Bearer {access_token}"})
    client.delete(f"/exams/{student_id}/P121/2024-09-19T07:38:46.871Z",headers= {"Authorization": f"Bearer {access_token}"})
    client.delete(f"/exams/{student_id}/M101/2024-09-19T07:38:46.871Z",headers= {"Authorization": f"Bearer {access_token}"})
    client.delete(f"/exams/{student_id}/M102/2024-09-19T07:38:46.871Z",headers= {"Authorization": f"Bearer {access_token}"})

    client.delete(f"/students/{student_id}",headers= {"Authorization": f"Bearer {access_token}"})
    client.delete("/courses/P120",headers= {"Authorization": f"Bearer {access_token}"})
    client.delete("/courses/P121",headers= {"Authorization": f"Bearer {access_token}"})
    client.delete("/courses/M101",headers= {"Authorization": f"Bearer {access_token}"})
    client.delete("/courses/M102",headers= {"Authorization": f"Bearer {access_token}"})
    client.delete("/students/2",headers= {"Authorization": f"Bearer {access_token}"})

