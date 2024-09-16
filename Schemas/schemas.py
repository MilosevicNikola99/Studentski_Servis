from datetime import datetime

from pydantic import BaseModel, conint


class StudentBase(BaseModel):
    ime : str
    prezime : str
    indeks : str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    naziv: str
    espb: int

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    sifra_predmeta : str

    class Config:
        from_attributes = True


class ExamBase(BaseModel):
    datum: datetime
    ocena: conint(ge=1, le=10)
    polozen: bool

class ExamCreate(ExamBase):
    student_id: int
    course_sifra: str

class Exam(ExamBase):
    student_id: int
    course_sifra: str
    datum: datetime

    class Config:
        from_attributes = True