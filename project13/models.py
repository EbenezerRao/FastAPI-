from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import base

class Client(base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, unique=True)
    budget = Column(Integer)

    # 🤝 The Python Magic: A client has many deliverables
    deliverables = relationship("Deliverable", back_populates="client")
    
class Deliverable(base):
    __tablename__ = 'deliverables'
    
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String)
    status = Column(String)
    client_id = Column(Integer, ForeignKey('clients.id'))
    
    client = relationship('Client', back_populates='deliverables')