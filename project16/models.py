from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import base

class Contributor(base):
    __tablename__ = "contributors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    wiki_username = Column(String, index=True)
    contributions = relationship('Article', back_populates='contributor', cascade="all, delete-orphan")
    
class Article(base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    word_count = Column(Integer)
    contributor_id = Column(Integer, ForeignKey('contributors.id'))
    
    contributor = relationship('Contributor', back_populates='contributions')