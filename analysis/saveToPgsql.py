#%% SAVE DATA TO POSTGRESQL DATABASE
import os
import asyncpg
import asyncio
import nest_asyncio
from datetime import datetime
from dotenv import load_dotenv
load_dotenv('.env')
nest_asyncio.apply()

#THE THREE TABLES ARE 
#last_six_weeks
    #stock_id SERIAL PRIMARY KEY
    #name VARCHAR,
    #last_fetched_date DATE,
    #prices VARCHAR

#risk_reward
    #stock_id SERIAL PRIMARY KEY
    #name VARCHAR,
    #risk FLOAT,
    #reward FLOAT

#png_files
    #name VARCHAR,
    #encode VARCHAR


#UPLOAD DATA TO POSTGRESQL DATABASE IN GOOGLE CLOUD
#USER AUTH FOR GOOGLE CLOUD DATABASE FROM ENVIRONMENT VARIABLES
user = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")
host = os.getenv("HOST")
    # stock_id SERIAL PRIMARY KEY,

schemas = {'df_last_six_weeks': '''
    name VARCHAR(255),
    lastFetched DATE,
    prices VARCHAR
''',
'df_stock_return_risk': '''
    name VARCHAR(255),
    risk NUMERIC,
    reward NUMERIC
''',
'df_encoded': '''
    name VARCHAR(255),
    encode VARCHAR
'''}

def typeClean(dataset, str):
    str_arr = str.strip().split(',')
    if dataset == 'df_last_six_weeks':
        for i in range(len(str_arr)):

            if i == 1:
                print(str_arr[1])

                str_arr[i] = datetime.fromisoformat(str_arr[i])
            elif str_arr[i] == '':
                str_arr[i] = None
            # else:
            #     str_arr[i] = float(str_arr[i])
    if dataset == 'df_stock_return_risk':
        for i in range(len(str_arr)):
            if i != 0 and str_arr[i] != '':
                str_arr[i] = float(str_arr[i])
            elif str_arr[i] == '':
                str_arr[i] = None
            # else:
            #     str_arr[i] = float(str_arr[i])
    return str_arr

csv_files = []
for file in os.listdir(os.getcwd()):
    if file.endswith('.csv' or '.png'):
        csv_files.append(file)

for dataset in csv_files:
    datasetName = dataset[:-4]
    if datasetName in schemas.keys():
        print(datasetName)
        tblName = dataset[3:-4]
        async def run():
            conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
            print('connected')
            await conn.execute(f'DROP TABLE IF EXISTS {datasetName}')
            await conn.execute(f'''
                    CREATE TABLE {datasetName} (
                        {schemas[datasetName]}
                    );
                ''')
            print(f'{datasetName} was created successfully')
            # copy prices to table using price header
            values = []
            with open(dataset, 'r') as f:
                next(f)
                for row in f:
                    values.append(tuple(typeClean(datasetName, row)))
                
            result = await conn.copy_records_to_table(
                datasetName, records=values
            )
            print(result, f'import to {datasetName} complete')

            await conn.close() #close the connection
        loop = asyncio.get_event_loop() #can also make single line
        loop.run_until_complete(run())
        print('all tables successfully imported')
# %%
