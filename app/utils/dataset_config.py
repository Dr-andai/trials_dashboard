import os
import pandas as pd
from app.models.models import Base, Author, Publication, Journal

# data directory
PROCESSED_DATA_DIR = 'data/processed/'

authors_data_path = 'models/model_data/authors.csv'
publications_data_path = 'models/model_data/publications.csv'
journals_data_path = 'models/model_data/journals.csv'

# model data
authors_df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, authors_data_path))
publications_df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, publications_data_path))
journals_df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, journals_data_path))


# Create dataset configuration
dataset_config = {
    Author: authors_df,
    Publication: publications_df,
    Journal: journals_df
}