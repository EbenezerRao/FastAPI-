from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    budget = Column(Integer)

    deliverables = relationship("Deliverable", back_populates="client")

class Deliverable(Base):
    __tablename__ = "deliverables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    client_id = Column(Integer, ForeignKey("clients.id"))

    client = relationship("Client", back_populates="deliverables")