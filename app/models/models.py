from sqlalchemy import Column, DateTime, String, Integer, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
metadata = Base.metadata

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    author_title = Column(String(60), unique=False)
    institution = Column(String(60), unique=False)

    publication = relationship('Publication', backref='author')
    journal = relationship('Journal', backref='author')

class Publication(Base):
     __tablename__ = 'publications'
     
     id = Column(Integer, primary_key=True)
     author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
     publication_title = Column(String, unique=False)
     year = Column(Integer, nullable=True, default=None)
     citations = Column(Integer, nullable= False)

class Journal(Base):
     __tablename__ = 'journals'
     
     id = Column(Integer, primary_key=True)
     author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
     citation = Column(String, nullable=True, unique=False)
     country = Column(String(200), nullable= True, unique=False)
     year = Column(Integer, nullable=True, default=None)
     impact_factor = Column(Integer, nullable= True)
    