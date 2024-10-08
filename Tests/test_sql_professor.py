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

def test_create_professor():
    response = client.post(
                    '/professors/',
                        json = {
                                  "ime": "Miroslav",
                                  "prezime": "Maric",
                                  "departman": "Racunarstvo i informatika"
                               }
                )
    assert response.status_code == 200
    assert response.json() == {
                                  "id" : 2,
                                  "ime": "Miroslav",
                                  "prezime": "Maric",
                                  "departman": "Racunarstvo i informatika"
                               }

def test_get_professor():
    response = client.get('/professors/2')
    assert response.status_code == 200, response.text
    assert response.json() == {
                                  "id" : 2,
                                  "ime": "Miroslav",
                                  "prezime": "Maric",
                                  "departman": "Racunarstvo i informatika"
                               }


def test_update_professor():
    response = client.put('/professors/2', json = {
                                  "ime": "Filip",
                                  "prezime": "Maric",
                                  "departman": "Racunarstvo i informatika"})
    assert response.status_code == 200, response.text
    assert response.json() == {
                                "id" : 2,
                                "ime": "Filip",
                                "prezime": "Maric",
                                "departman": "Racunarstvo i informatika"}

def test_delete_professor():
    response = client.delete('/professors/2')
    assert response.status_code == 200, response.text
    assert response.json() == {"Professor deleted" : True}
