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
    echo=False,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=async_engine , class_=AsyncSession)


#Base.metadata.create_all(bind=engine)
# Override the get_db function for tests

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
async def test_create_courses():
    auth = client.post("/login/user",data={"grant_type" : "password","username": "admin", "password": "password"} )
    assert auth.status_code == 200
    access_token = auth.json().get("access_token")

    response = client.post(
        "/courses/",
        json={
                "naziv": "Programiranje1",
                "espb": 6,
                "profesor_id": 1,
                "sifra_predmeta": "P120"
        },
        headers= {"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["naziv"] == "Programiranje1"
    assert data["espb"] == 6
    assert data["sifra_predmeta"] == "P120"
    assert data["profesor_id"] == 1

@pytest.mark.asyncio
async def test_get_course():

    response = client.get("/courses/P120")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["naziv"] == "Programiranje1"
    assert data["espb"] == 6
    assert data["sifra_predmeta"] == "P120"
    assert data["profesor_id"] == 1

@pytest.mark.asyncio
async def test_get_courses_by_profesor_id():

    response = client.get("/courses/", params={'profesor_id': 1})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == [
                        {'sifra_predmeta': 'P120',
                         'profesor_id': 1,
                         'naziv': 'Programiranje1',
                         'espb': 6,
                    'profesor':
                        {'prezime': 'Janicic',
                         'ime': 'Predrag',
                         'departman': 'Racunarstvo i informatika',
                         'id': 1,
                         'user_id': 3}}]

@pytest.mark.asyncio
async def test_get_courses_by_naziv():

    auth = client.post("/login/user",data={"grant_type" : "password","username": "admin", "password": "password"} )
    assert auth.status_code == 200
    access_token = auth.json().get("access_token")

    response = client.get("/courses/",
                          params={'naziv': 'Programiranje1'},
                          headers={"Authorization": f"Bearer {access_token}"}
                          )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == [
                        {'sifra_predmeta': 'P120',
                         'profesor_id': 1,
                         'naziv': 'Programiranje1',
                         'espb': 6,
                    'profesor':
                        {'prezime': 'Janicic',
                         'ime': 'Predrag',
                         'departman': 'Racunarstvo i informatika',
                         'id': 1,
                         'user_id': 3}}]

@pytest.mark.asyncio
async def test_get_courses_by_departman():

    response = client.get("/courses/",
                          params={'departman': 'Racunarstvo i informatika'},
                          )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == [
                        {'sifra_predmeta': 'P120',
                         'profesor_id': 1,
                         'naziv': 'Programiranje1',
                         'espb': 6,
                    'profesor':
                        {'prezime': 'Janicic',
                         'ime': 'Predrag',
                         'departman': 'Racunarstvo i informatika',
                         'id': 1,
                         'user_id': 3}}]

@pytest.mark.asyncio
async def test_update_courses():

    auth = client.post("/login/user",data={"grant_type" : "password","username": "admin", "password": "password"} )
    assert auth.status_code == 200
    access_token = auth.json().get("access_token")

    response = client.put("/courses/P120",
                          json={
                                "naziv": "Programiranje2",
                                "espb": 6,
                                "profesor_id": 1,
                          },
                          headers={"Authorization": f"Bearer {access_token}"}
                          )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["naziv"] == "Programiranje2"
    assert data["espb"] == 6
    assert data["sifra_predmeta"] == "P120"
    assert data["profesor_id"] == 1

@pytest.mark.asyncio
async def test_delete_course():

    auth = client.post("/login/user",data={"grant_type" : "password","username": "admin", "password": "password"} )
    assert auth.status_code == 200
    access_token = auth.json().get("access_token")

    response = client.delete("/courses/P120" ,
                             headers={"Authorization": f"Bearer {access_token}"}
                             )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == {"Course deleted" : True}