from sqlalchemy import Column, DateTime, String, Integer, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
metadata = Base.metadata

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(60), unique=True)
    title = Column(String(60), unique=True)
    instituition = Column(String(60), unique=True)

    publication = relationship('Publication', backref='author_name')
    journal = relationship('Journal', backref='author_name')

class Publication(Base):
    __tablename__ = 'publications'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    title = Column(String(200), unique=True)
    year = Column(Integer, nullable= False)
    citations = Column(Integer, nullable= False)

class Journal(Base):
    __tablename__ = 'journals'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    title = Column(String(200), unique=True)
    year = Column(Integer, nullable= False)
    factor = Column(Integer, nullable= False)
    