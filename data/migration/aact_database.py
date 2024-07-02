import psycopg2
import pandas as pd
from sqlalchemy import create_engine

# Create own account, then Connect to AACT database
source_conn = psycopg2.connect(
    dbname="aact",
    user="andai",
    password="Clinical%2024",
    host="aact-db.ctti-clinicaltrials.org",
    port="5432"
)
source_cursor = source_conn.cursor()

# Fetch data, set limit to save on time
query = """
SELECT 
	countries.nct_id AS nct_id,
	studies.study_first_submitted_date AS first_date,
	facilities.name AS facility_name,
	facilities.city AS city,
	facility_investigators.name AS investigator,
	facility_investigators.role AS investigator_role,
	sponsors.name AS sponsor_name,
    sponsors.lead_or_collaborator AS lead_or_collaborator,
	conditions.downcase_name AS downcase_name,
	detailed_descriptions AS description
	
	
	FROM countries
	INNER JOIN facilities USING (nct_id)
	INNER JOIN sponsors USING (nct_id)
	INNER JOIN conditions USING (nct_id)
	INNER JOIN facility_investigators USING (nct_id)
	INNER JOIN detailed_descriptions USING (nct_id)
	INNER JOIN studies USING (nct_id)
	WHERE countries.name = 'Kenya'
		AND studies.study_first_submitted_date BETWEEN '2020-01-01' AND '2023-12-31'
		ORDER BY first_date DESC;
        -- LIMIT 1000;

"""
source_cursor.execute(query)

data = source_cursor.fetchall()
colnames = [desc[0] for desc in source_cursor.description]

# save to raw data
df = pd.DataFrame(data, columns=colnames)
df.to_csv('data/raw/aact_folder/aact_data', index=False)

source_cursor.close()
source_conn.close()