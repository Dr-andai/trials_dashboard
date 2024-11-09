# Project Overview
This project explores the relationship between clinical trials and the research profiles of authors, with a focus on investigators conducting trials in Kenya. Data is sourced from https://aact.ctti-clinicaltrials.org/ and https://serpapi.com/google-scholar-api preprocessed, and visualized on a Shiny dashboard.


## Key steps
- Pulling data from AACT using SQL
- Pulling data from Google Scholar API
- Setting up a Postgresql database on Docker
- Data Cleaning using Jupyter Notebook
- Data deployment on Shiny Dashboard

The following Dashboard project displays different clinical trials and associated Sponsors profile

# Project Strutcure
- **app/**: Contains the app files.
- **data/**: Contains the data files.
  - **raw/**: Raw data files.
  - **processed/**: Processed data files.
- **notebokes/**: Contains the data cleaning ipynbs.

Project status: continuing