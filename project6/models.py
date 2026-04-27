from sqlalchemy import Column, Integer, String
from database import Base

class Sponsors(Base):
    __tablename__ = 'sponsors'

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    tier = Column(String)