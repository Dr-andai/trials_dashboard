import os
import pandas as pd

from sqlalchemy.orm import Session

from app.config import SessionLocal, engine
from app.models.models import Base, Author
from app.utils.logger import setup_logging

# load data
PROCESSED_DATA_DIR = 'data/processed/'
authors_data_path = 'model_data/authors.csv'

authors_df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, authors_data_path))

# create db session
session = SessionLocal()

# Seeder
def seed_author(model, df):
    model_fields = set(model.__table__.columns.keys())
    df_columns = set(df.columns)

    # check column names
    if not df_columns.issubset(model_fields):
        raise ValueError(f"No matching fields: {df_columns} to {model_fields}")
    
    for _, row in df.iterrows():
        record_data = {column: row[column] for column in df_columns}
        record = model(**record_data)
        session.add(record)
    session.commit()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    logger = setup_logging('author_seeding.log')
    try:
        seed_author(Author, authors_df)
        logger.info("Seeding completed Successfully")
    except ValueError as e:
        logger.error(f"Error in seeding data: {e}")
    finally:
        session.close()