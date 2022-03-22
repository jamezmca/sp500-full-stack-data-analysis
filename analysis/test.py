# %% Imports
import os
import asyncpg
import asyncio
import nest_asyncio
from dotenv import load_dotenv
load_dotenv('.env')
nest_asyncio.apply()
#%% SAVE DATA TO POSTGRESQL DATABASE
# Read Env variables
user = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")
host = os.getenv("HOST")

csv_files = [] #Get a list of CSV files
for file in [f for f in os.listdir(os.getcwd()) if f.endswith('.csv')]:
    csv_files.append(file)

for dataset in csv_files:
    datasetName = dataset[:-4] #remove the .csv suffix
    async def run():
        conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
        await conn.execute(f'DROP TABLE IF EXISTS {datasetName}') #Drop table if it already exists
        await conn.execute(f'''
                CREATE TABLE insert_table_name (
                    name VARCHAR(255),
                    lastFetched DATE,
                    price VARCHAR
                );
            ''')
        values = []
        with open(dataset, 'r') as f: #read CSV row by row and convert to a tuple
            next(f)
            for row in f:
                values.append(tuple(row))
        result = await conn.copy_records_to_table(
            datasetName, records=values
        )
        await conn.close() #close the connection
    loop = asyncio.get_event_loop().run_until_complete(run()) 
    print('Successfully written .csv to PSQL table')
# %%
