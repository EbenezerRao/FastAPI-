from sqlalchemy import Column, Integer, String
from database import Base

class Speaker(Base):
    __tablename__ = 'speakers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    topic = Column(String)