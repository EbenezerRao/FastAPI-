from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Hacker(Base):
    __tablename__ = 'hackers'
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String, index=True)
    is_checked_in = Column(Boolean, index=True)