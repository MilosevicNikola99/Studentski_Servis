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
    profesor_id: int
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
    sifra_predmeta: str

class Exam(ExamBase):
    student_id: int
    sifra_predmeta: str
    datum: datetime

    class Config:
        from_attributes = True

class ProfessorBase(BaseModel):
        ime: str
        prezime: str
        departman: str

class ProfessorCreate(ProfessorBase):
    pass

class Professor(ProfessorBase):
    id: int

    class Config:
        from_attributes = True

class EnrollmentBase(BaseModel):
    student_id: int
    sifra_predmeta: str
    datum_upisa: datetime

class EnrolmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):

    class Config:
        from_attributes = True