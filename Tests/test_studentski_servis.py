from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..Database.database import Base
from ..studentski_servis import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_test_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_statistics():
    response = client.post("/students/",
                    json={
                        "ime": "Petar",
                        "prezime": "Petrovic",
                        "indeks": "100-2023"
                    },
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
                })

    client.post("/courses/",
                json={
                    "naziv": "Programiranje2",
                    "espb": 6,
                    "sifra_predmeta": "P121",
                    "profesor_id": 1
    })

    client.post("/courses/",
                json={
                    "naziv": "Analiza1",
                    "espb": 6,
                    "sifra_predmeta": "M101",
                    "profesor_id": 1
                })

    client.post("/courses/",
                json={
                    "naziv": "Analiza2",
                    "espb": 6,
                    "sifra_predmeta": "M102",
                    "profesor_id": 1
                })
    client.post("/exams/" , json={
                    "datum": "2024-09-19T07:38:46.871Z",
                    "ocena": 7,
                    "polozen": True,
                    "student_id": student_id,
                    "sifra_predmeta": "P120"
        })
    client.post("/exams/" , json={
                    "datum": "2024-09-19T07:38:46.871Z",
                    "ocena": 5,
                    "polozen": False,
                    "student_id": student_id,
                    "sifra_predmeta": "P121"
        })
    client.post("/exams/" , json={
                    "datum": "2024-09-19T07:38:46.871Z",
                    "ocena": 8,
                    "polozen": True,
                    "student_id": student_id,
                    "sifra_predmeta": "M101"
        })
    client.post("/exams/" , json={
                    "datum": "2024-09-19T07:38:46.871Z",
                    "ocena": 5,
                    "polozen": False,
                    "student_id": student_id,
                    "sifra_predmeta": "M102"
        })

    respone = client.get(f"/statistics/{student_id}/")
    assert respone.status_code == 200
    assert respone.json() == {"ESPB" : 12, "Polozio" :2}


    client.delete(f"/exams/{student_id}/P120/2024-09-19T07:38:46.871Z")
    client.delete(f"/exams/{student_id}/P121/2024-09-19T07:38:46.871Z")
    client.delete(f"/exams/{student_id}/M101/2024-09-19T07:38:46.871Z")
    client.delete(f"/exams/{student_id}/M102/2024-09-19T07:38:46.871Z")

    client.delete(f"/students/{student_id}")
    client.delete("/courses/P120")
    client.delete("/courses/P121")
    client.delete("/courses/M101")
    client.delete("/courses/M102")

