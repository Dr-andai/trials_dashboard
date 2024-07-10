import os
import pandas as pd

from sqlalchemy.orm import Session
from app.models.models import Base, Author, Journal, Publication
from app.config import engine, SessionLocal
from app.utils.dataset_config import dataset_config
from app.utils.logger import setup_logging

def seed_data(model, df, authors):
    # excluding id as it's an auto-increment
    if model == Author:
        model_fields = set(model.__table__.columns.keys()) - {'id'}
        df_columns = set(df.columns)
    else:
        model_fields = set(model.__table__.columns.keys()) - {'id', 'author_id'}
        df_columns = set(df.columns) - {'author'}

    # Check if data columns match model fields
    if not df_columns.issubset(model_fields):
        raise ValueError (f"No matching fields: {df_columns} to {model_fields}")
    
    for _, row in df.iterrows():
        # Mapa Data Frame columns to Model Fields
        record_data = {column: row[column] for column in df_columns}

        if model != Author:
        # Fetch Author id from the Authors dictionary using the 'author' column in the Data Frame
            authors_name = row['author']
            if authors_name:
                author_id = authors.get(authors_name)
                if author_id is None:
                    raise ValueError(f"No author_id found for the author: {authors_name}")
                # add the author_id to the record data
                record_data['author_id'] = author_id

        # create an instance of the model
        try:
            record = model(**record_data)
            session.add(record)
        except (OverflowError, ValueError) as e:
            logger.error(f"Data value out of range or invalid data type: {e}, Data: {record_data}")
            continue
    
    session.commit()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    
    logger = setup_logging('seeding.log')

    # Create database session
    session = SessionLocal()

    try:
    # Fetch all authors and store them in a dictionary
        authors = {author.name: author.id for author in session.query(Author).all()}
    
        for model, dataframe in dataset_config.items():
            try:
                logger.info(f"Seeding {model.__tablename__}...")
                # Check DataFrame stats
                logger.info(f"{model.__tablename__} DataFrame stats: {dataframe.describe(include='all')}")

                seed_data(model, dataframe, authors)
                logger.info(f"Seeding the {model.__tablename__} completed successfully.")
            except ValueError as e:
                logger.error(f"Error in seeding {model.__tablename__}: {e}")
    finally:
        session.close()