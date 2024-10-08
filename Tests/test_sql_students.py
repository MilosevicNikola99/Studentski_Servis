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

def test_create_student():
    response = client.post(
        "/students/",
        json={
                "ime": "Petar",
                "prezime": "Petrovic",
                "indeks": "100-2023"
            }   ,
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["ime"] == "Petar"
    assert data["prezime"] == "Petrovic"
    assert data["indeks"] == "100-2023"
    assert "id" in data
    student_id = data["id"]

    response = client.get(f"/students/{student_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["ime"] == "Petar"
    assert data["prezime"] == "Petrovic"
    assert data["indeks"] == "100-2023"
    assert data["id"] == student_id

def test_update_student():
    response = client.put("/students/1", json={
                "ime": "Luka",
                "prezime": "Lukic",
                "indeks": "100-2023"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["ime"] == "Luka"
    assert data["prezime"] == "Lukic"
    assert data["indeks"] == "100-2023"
    assert data["id"] == 1

def test_delete_student():
    response = client.delete("/students/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == {"Student deleted" : True}