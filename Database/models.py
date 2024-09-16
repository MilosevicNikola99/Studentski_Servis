from datetime import datetime
from typing import List

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, column
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy import ForeignKeyConstraint

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

    student_id : Mapped[int] = mapped_column( primary_key=True)
    sifra_predmeta : Mapped[str] = mapped_column(primary_key=True)
    datum : Mapped[datetime] = mapped_column(primary_key=True)
    ocena : Mapped[int]
    polozen : Mapped[bool]

    __table_args__ = (
        ForeignKeyConstraint(['student_id'], ['student.id'], name='fk_student_id'),
        ForeignKeyConstraint(['sifra_predmeta'], ['course.sifra_predmeta'], name='fk_course_sifra_predmeta'),
    )

    student = relationship("Student", back_populates="exams")
    course = relationship("Course", back_populates="exams")

