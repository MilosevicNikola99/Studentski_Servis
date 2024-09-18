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

def test_create_courses():
    response = client.post(
        "/courses/",
        json={
                "naziv": "Programiranje1",
                "espb": 6,
                "sifra_predmeta": "P120"
        } ,
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["naziv"] == "Programiranje1"
    assert data["espb"] == 6
    assert data["sifra_predmeta"] == "P120"


def test_get_courses():
    response = client.get(f"/courses/P120")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["naziv"] == "Programiranje1"
    assert data["espb"] == 6
    assert data["sifra_predmeta"] == "P120"

def test_update_courses():
    response = client.put("/courses/P120", json={
                "naziv": "Programiranje2",
                "espb": 6,
                "sifra_predmeta": "P121"
        } )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["naziv"] == "Programiranje2"
    assert data["espb"] == 6
    assert data["sifra_predmeta"] == "P120"

def test_delete_student():
    response = client.delete("/courses/P120")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == {"Course deleted" : True}