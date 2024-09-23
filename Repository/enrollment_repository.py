from datetime import datetime
from fastapi import HTTPException, Depends


from ..dependencies import get_db
from ..Database import models, database
from ..Schemas import schemas

def get_enrollment_repository(db: database.SessionLocal = Depends(get_db)):
    return EnrollmentRepository(db)

class EnrollmentRepository:

    def __init__(self , db ):
        self.db = db

    def get_enrollments_by_id(self, id : int):
        return self.db.query(models.Enrollment).filter(id == models.Enrollment.student_id).all()

    def get_enrollments_by_sifra(self, sifra_predmeta : str):
        return self.db.query(models.Enrollment).filter(sifra_predmeta == models.Enrollment.sifra_predmeta).all()


    def get_enrollments_by_datum_upisa(self, datum_upisa : datetime):
        return self.db.query(models.Enrollment).filter(datum_upisa == models.Enrollment.datum_upisa).all()

    def get_enrollment(self, student_id : int, sifra_predmeta : str, datum_upisa : datetime):
        return self.db.query(models.Enrollment).filter(student_id == models.Enrollment.student_id,
                                                  sifra_predmeta == models.Enrollment.sifra_predmeta,
                                                  datum_upisa == models.Enrollment.datum_upisa).first()

    def get_enrollments(self):
        return self.db.query(models.Enrollment).all()

    def create_enrollment(self, enrollment : schemas.EnrolmentCreate):
        db_enrollment = models.Enrollment(student_id = enrollment.student_id,sifra_predmeta = enrollment.sifra_predmeta,datum_upisa = enrollment.datum_upisa)
        try:
            self.db.add(db_enrollment)
            self.db.commit()
        except:
            self.db.rollback()
            raise HTTPException(status_code=400, detail='Database Error : create enrollment failed')

        self.db.refresh(db_enrollment)
        return db_enrollment


    def update_enrollment(self, enrollment, up_enrollment):
        try:
            enrollment.student_id = up_enrollment.student_id
            enrollment.sifra_predmeta = up_enrollment.sifra_predmeta
            enrollment.datum_upisa = up_enrollment.datum_upisa
            self.db.commit()
        except:
            self.db.rollback()
            raise HTTPException(status_code=400, detail='Database Error : update enrollment failed')

        self.db.refresh(enrollment)
        return enrollment


    def delete_enrollment(self, enrollment):
        try:
            self.db.delete(enrollment)
            self.db.commit()
            return { "Enrollment Deleted" : True}
        except:
            self.db.rollback()
            raise HTTPException(status_code=400, detail='Database Error : delete enrollment failed')
