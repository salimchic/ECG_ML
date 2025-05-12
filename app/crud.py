from sqlalchemy.orm import Session
from app import models


def create_edf_data(db: Session, edf_data: dict):
    db_edf = models.EDFData(**edf_data)
    db.add(db_edf)
    db.commit()
    db.refresh(db_edf)
    return db_edf
