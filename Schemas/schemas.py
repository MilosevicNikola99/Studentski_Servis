from datetime import datetime
from typing import Optional

from pydantic import BaseModel, conint, ConfigDict ,Field




class StudentBase(BaseModel):
    ime : str
    prezime : str
    indeks : str

class StudentCreate(StudentBase):
    user_id : int

class Student(StudentBase):
    id: int = Field(..., ge=1, le=10000)

    model_config = ConfigDict(from_attributes=True)



class ExamBase(BaseModel):
    datum: datetime
    ocena: conint(ge=1, le=10)
    polozen: bool

class ExamCreate(ExamBase):
    student_id: int = Field(..., ge=1, le=10000)
    sifra_predmeta: str

class Exam(ExamBase):
    student_id: int = Field(..., ge=1, le=10000)
    sifra_predmeta: str
    datum: datetime

    model_config = ConfigDict(from_attributes=True)

class ProfessorBase(BaseModel):
        ime: str
        prezime: str
        departman: str

class ProfessorCreate(ProfessorBase):
    user_id : int

class Professor(ProfessorBase):
    id: int = Field(..., ge=1, le=10000)

    model_config = ConfigDict(from_attributes=True)

class EnrollmentBase(BaseModel):
    student_id: int = Field(..., ge=1, le=10000)
    sifra_predmeta: str
    datum_upisa: datetime

class EnrolmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):

    model_config = ConfigDict(from_attributes=True)


class CourseBase(BaseModel):
    naziv: str
    espb: int
    profesor_id: int


class CourseCreate(CourseBase):
    sifra_predmeta: str


class Course(CourseCreate):

    profesor: Optional[ProfessorBase]
    model_config = ConfigDict(from_attributes=True)


class UserStudentBase(BaseModel):
    username: str
    student_id: int

class UserStudentCreate(UserStudentBase):
    pass

class UserStudent(UserStudentBase):
    id : int = Field(..., ge=1, le=10000)

    model_config = ConfigDict(from_attributes=True)

class UserProfessorBase(BaseModel):
    username: str
    professor_id: int

class UserProfessorCreate(UserProfessorBase):
    pass

class UserProfessor(UserProfessorBase):
    id: int = Field(..., ge=1, le=10000)

    model_config = ConfigDict(from_attributes=True)

class Admin(BaseModel):
    id: int = Field(..., ge=1, le=10000)
    username: str

    model_config = ConfigDict(from_attributes=True)

class User(BaseModel):
    id: int = Field(..., ge=1, le=10000)
    username: str
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)
