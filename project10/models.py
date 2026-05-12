from sqlalchemy import Column, Integer, String
from database import Base

class Tracker(Base):
    __tablename__ = 'leads'
    
    client_name = Column(String, primary_key=True, index=True)
    project_name = Column(String, index=True)
    budget = Column(Integer)