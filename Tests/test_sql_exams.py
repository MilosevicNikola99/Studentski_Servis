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

def test_create_exam():
    response = client.post(
        "/exams/",
        json={
                  "datum": "2024-09-18T13:02:21.702Z",
                  "ocena": 6,
                  "polozen": True,
                  "student_id": 1,
                  "sifra_predmeta": "P120"
        } ,
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["datum"] == "2024-09-18T13:02:21.702000"
    assert data["ocena"] == 6
    assert data["student_id"] == 1
    assert data["sifra_predmeta"] == "P120"


def test_get_courses():
    response = client.get("/exams/1/P120/2024-09-18T13:02:21.702Z")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["datum"] == "2024-09-18T13:02:21.702000"
    assert data["ocena"] == 6
    assert data["student_id"] == 1
    assert data["sifra_predmeta"] == "P120"

def test_update_courses():
    response = client.put("/exams/1/P120/2024-09-18T13:02:21.702Z", json= {
                              "datum": "2024-09-18T13:04:24.978Z",
                              "ocena": 9,
                              "polozen": True
                            })
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["ocena"] == 9
    assert data["polozen"] == True

def test_delete_student():
    response = client.delete("/exams/1/P120/2024-09-18T13:02:21.702Z")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == {"Exam deleted" : True}