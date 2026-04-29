from sqlalchemy import Column, Integer, String
from database import Base, engine

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    deliverable = Column(String, nullable=False) # Spelled correctly!
    status = Column(String, default="Pending")

# This line tells Postgres to build the table immediately when the app starts
