from datetime import datetime
from typing import List

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, column
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.testing.schema import mapped_column

from .database import Base


class Student(Base):
    __tablename__ = 'student'

    id: Mapped[int] = mapped_column(primary_key=True)
    ime : Mapped[str]
    prezime : Mapped[str]
    indeks : Mapped[str] = mapped_column(unique=True, nullable=False)

    exams : Mapped[List["Exam"]] = relationship("Exam", back_populates="student")

class Course(Base):
    __tablename__ = 'course'

    sifra_predmeta : Mapped[str] = mapped_column(primary_key=True)
    naziv : Mapped[str]
    espb : Mapped[int]

    exams : Mapped[List["Exam"]] = relationship("Exam", back_populates="course")

class Exam(Base):
    __tablename__ = 'exam'

    student_id : Mapped[int] = mapped_column(ForeignKey('student.id'), primary_key=True)
    course_sifra : Mapped[str] = mapped_column(ForeignKey('course.sifra_predmeta'), primary_key=True)
    datum : Mapped[datetime] = mapped_column(primary_key=True)
    ocena : Mapped[int]
    polozen : Mapped[bool]

    student = relationship("Student", back_populates="exams")
    course = relationship("Course", back_populates="exams")

