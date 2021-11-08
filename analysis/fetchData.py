#%% FETCH DATA FROM YFINANCE (might also want to fetch sp500)
#source myenv/bin/activate
import os
import numpy as np
import pandas as pd
# import pytrends
import yfinance as yf
import math
import requests
from datetime import datetime
from pytrends.request import TrendReq

def clenseArray(array): #CLEAN HEADERS/COL NAMES
    array = [x.lower().replace(" ", "_")\
        .replace("-","_").replace("?","_").replace(r"/", "_").replace('.', '').replace("\'s", 's')\
        .replace(")", "").replace(r"(", "").replace("%", "").replace('all', 'all_').replace(',',"")\
        .replace("?", "").replace("\\", "_").replace("$","").replace('&',"and").replace("'", '').replace("3m", '"3m"') for x in array]
    return array


#CREATE DICTIONARY OF NAMES
sp_wiki_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
sp_wiki_df_list = pd.read_html(sp_wiki_url)
sp_df = sp_wiki_df_list[0]
sp_ticker_list = list(sp_df['Symbol'].values)
sp_name_list = list(sp_df['Security'].values)
dictionary = dict(zip(clenseArray(sp_ticker_list), clenseArray(sp_name_list)))
df = pd.DataFrame.from_dict(dictionary, orient="index")
df.to_csv("dictionary.csv")

#DOWNLOAD DATA FROM YFINANCE
df_2021 = yf.download(sp_ticker_list, start="2015-01-01")

#%%
df_2015 = yf.download(sp_ticker_list, start="2010-01-01", end="2015-01-01")

#%%
df_2010 = yf.download(sp_ticker_list, start="2005-01-01", end="2010-01-01")


#%%
df_2005 = yf.download(sp_ticker_list, start="2000-01-01", end="2005-01-01")

#TAKE ADJ CLOSE VALUES AND TURN INTO DF
def checkIfNan(df): 
    #could also use .tal
    fin = df.iloc[-1]
    if math.isnan(fin[1]) and math.isnan(fin[5]):
        return df.iloc[:-1]
    return df

def saveToCSV(df, name): 
    df_prices = checkIfNan(df['Adj Close'])
    df_prices.columns = clenseArray(df_prices.columns)
    df_prices.to_csv(f'{name}.csv', header=df_prices.columns, index=True , encoding='utf-8')
    return 
# df_sp_prices = checkIfNan(df_sp_values['Adj Close'])
# df_sp_prices.columns = clenseArray(df_sp_prices.columns)

# #SAVE TO CSV FILE
# df_sp_prices.to_csv('df_sp_prices.csv', header=df_sp_prices.columns, index=True , encoding='utf-8')

saveToCSV(df_2021, "df_2021")
saveToCSV(df_2015, "df_2015")
saveToCSV(df_2010, "df_2010")
saveToCSV(df_2005, "df_2005")
print('Fetch Data Complete')


# %%
