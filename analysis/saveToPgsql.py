#%% SAVE DATA TO POSTGRESQL DATABASE
import os
import asyncpg
import asyncio
import nest_asyncio
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('.env')
nest_asyncio.apply()

#UPLOAD DATA TO POSTGRESQL DATABASE IN GOOGLE CLOUD
#USER AUTH FOR GOOGLE CLOUD DATABASE FROM ENVIRONMENT VARIABLES
user = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")
host = os.getenv("HOST")

data_sets = ['df_sp_prices.csv', 'df_sp_searches.csv', '']

csv_files = []
for file in os.listdir(os.getcwd()):
    if file.endswith('.csv' or '.png'):
        csv_files.append(file)

for dataset in csv_files:
    if dataset in data_sets:

        def createTableSchema(dataf):
            #SCHEMA FOR PRICE DATa
            col_str_two = ''
            print(dataf.columns)
            for stock_label in dataf.columns:
                print(stock_label)
                if stock_label.lower() == 'date':
                    print('howdy')
                    col_str_two = col_str_two + f'{stock_label.lower()} ' + 'DATE, ' 
                elif stock_label == "'3m'":
                    print('hi')
                    col_str_two = col_str_two + f'"{stock_label.lower()[1:-1]}" ' + 'FLOAT, '  
                else:
                    print('ahoha')
                    col_str_two = col_str_two + f'{stock_label} ' + 'FLOAT, ' 

            print('done')
            return col_str_two[:-2]

        def typeClean(str):
            str_arr = str.strip().split(',')
            
            for i in range(len(str_arr)):
                if i == 0:
                    str_arr[i] = datetime.fromisoformat(str_arr[i])
                elif str_arr[i] == '':
                    str_arr[i] = None
                else:
                    str_arr[i] = float(str_arr[i])
            return str_arr


        tblName = dataset[3:-4]
        async def run():
            conn = await asyncpg.connect(user=user, password=password, database=database, host=ip)
            print('connected')
            await conn.execute(f'DROP TABLE IF EXISTS {tblName}')
            await conn.execute(f'''
                    CREATE TABLE {tblName} (
                        {createTableSchema(eval(dataset[0:-4]))}
                    );
                ''')
            print(f'{tblName} was created successfully')
            # copy prices to table using price header
            values = []
            with open(dataset, 'r') as f:
                next(f)
                for row in f:
                    values.append(tuple(typeClean(row)))
                
            result = await conn.copy_records_to_table(
                tblName, records=values
            )
            print(result, f'import to {tblName} complete')

            await conn.close() #close the connection
        loop = asyncio.get_event_loop() #can also make single line
        loop.run_until_complete(run())
        print('all tables successfully imported')