import os
from models.models import (Author, Publication, Journal)
from config import SessionLocal
import pandas as pd

def fetch_data(authors, model, columns=None, session=None):
    if session is None:
        session = SessionLocal()

    query = session.query(Author.name.label('author'))

    if columns is None:
        model_columns = model.__table__.columns.keys()
        columns = [col for col in model_columns if col not in ('id', 'author_id')]
    
    for column in columns:
        query = query.add_columns(getattr(model, column).label(column))
    
    query = query.join(Author, model.author_id == Author.id)
    query = query.filter(Author.id.in_(authors))

    results = query.all()
    column_labels = ['author'] + columns
    df = pd.DataFrame(results, columns=column_labels)

    return df

def fetch_publications(authors, columns=None):
    with SessionLocal() as session:
        if not authors:
            authors = [id for id, name in session.query(Author.id, Author.name).all()]
        return fetch_data(authors, Publication, columns, session)
        
def fetch_journals(authors, columns=None):
    with SessionLocal() as session:
        if not authors:
            authors = [c.id for c in session.query(Author).all()]
        return fetch_data(authors, Journal, columns, session)

def get_author_dict():
    session = SessionLocal()
    authors = session.query(Author.id, Author.name).all()
    session.close()
    return {str(id): name for id, name in authors}