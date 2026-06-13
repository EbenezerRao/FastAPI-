from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    enrollment_no = Column(String, unique=True, nullable=False)
    score = relationship('StudentScore', back_populates='student', cascade='all, delete-orphan')    
    
class StudentScore(Base):
    __tablename__ = 'student_scores'
    
    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'))
    student = relationship('Student', back_populates='score')