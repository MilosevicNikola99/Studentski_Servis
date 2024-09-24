
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

def test_create_enrollment():
    client.post(
        "/students/",
        json={
                "ime": "Mitar",
                "prezime": "Jovanovic",
                "indeks": "101-2023"
            }   ,
    )
    client.post(
        "/courses/",
        json={
                "naziv": "ProjBP",
                "espb": 6,
                "profesor_id": 1,
                "sifra_predmeta": "P144"
        } ,
    )

    response = client.post("/enrollments/",
                           json = {
                                      "student_id": 1,
                                      "sifra_predmeta": "P144",
                                      "datum_upisa": "2024-09-24T10:11:35.514Z"
                                }
                           )

    assert response.status_code == 200
    assert response.json() == {
                                      "student_id": 1,
                                      "sifra_predmeta": "P144",
                                      "datum_upisa": "2024-09-24T10:11:35.514000"
                                }

def test_get_enrollment():
    response = client.get("/enrollments/")
    assert response.status_code == 200
    assert response.json() == [{
                                      "student_id": 1,
                                      "sifra_predmeta": "P144",
                                      "datum_upisa": "2024-09-24T10:11:35.514000"
                                }]

# def test_update_enrollment():
#     response = client.put("/enrollments/1/P144/2024-09-24T10:11:35.514Z",
#                           json = {
#   "student_id": 5,
#   "sifra_predmeta": "P120",
#   "datum_upisa": "2024-09-16T13:57:28.963000"
# })
#     assert response.status_code == 200
#     assert response.json() == {
#                                       "student_id": 1,
#                                       "sifra_predmeta": "P145",
#                                       "datum_upisa": "2024-09-24T10:11:35.514000"
#                                 }

def test_delete_enrollment():
    response = client.delete('/enrollments/1/P144/2024-09-24T10:11:35.514000')
    assert response.status_code == 200, response.text
    assert response.json() == {"Enrollment deleted" : True}
    client.delete('/students/1')
    client.delete('/courses/P144')




