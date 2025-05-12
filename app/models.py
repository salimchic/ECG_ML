from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base


class EDFData(Base):
    __tablename__ = "edf_data"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    channel_count = Column(Integer)
    sampling_freq = Column(Float)
    duration = Column(Float)
    timestamp = Column(DateTime)
