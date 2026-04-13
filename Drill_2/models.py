from sqlalchemy import Column, Integer, String
from .database import Base

class Destination(Base):
    __tablename__ = 'destinations'

    id = Column(String, primary_key=True, index=True)
    city_name = Column(String, index=True)
    planned_budget = Column(Integer, index=True)