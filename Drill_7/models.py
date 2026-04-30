from sqlalchemy import Column, Integer, String, Float
from database import Base

class Colleges(Base):
    __tablename__ = 'colleges'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    city = Column(String, index=True)
    rating = Column(Float, index=True)