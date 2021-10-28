#%% FETCH DATA FROM YFINANCE
#source myenv/bin/activate
import os
import numpy as np
import pandas as pd
import pytrends
import yfinance as yf
import requests
from datetime import datetime
from pytrends.request import TrendReq

def clenseArray(array): #CLEAN HEADERS/COL NAMES
    array = [x.lower().replace(" ", "_")\
        .replace("-","_").replace("?","_").replace(r"/", "_").replace('.', '').replace("\'s", 's')\
        .replace(")", "").replace(r"(", "").replace("%", "").replace('all', 'all_')\
        .replace("?", "").replace("\\", "_").replace("$","").replace('&',"and").replace("'", '').replace("3m", '"3m"') for x in array]
    return array


#CREATE DICTIONARY OF NAMES
sp_wiki_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
sp_wiki_df_list = pd.read_html(sp_wiki_url)
print(sp_wiki_df_list)
sp_df = sp_wiki_df_list[0]
sp_ticker_list = list(sp_df['Symbol'].values)
sp_name_list = list(sp_df['Security'].values)
dictionary = dict(zip(clenseArray(sp_ticker_list), clenseArray(sp_name_list)))
df = pd.DataFrame.from_dict(dictionary, orient="index")
df.to_csv("dictionary.csv")

#DOWNLOAD DATA FROM YFINANCE
df_sp_values = yf.download(sp_ticker_list, start="2016-01-01")

#TAKE ADJ CLOSE VALUES AND TURN INTO DF
df_sp_prices = df_sp_values['Adj Close']
df_sp_prices.columns = clenseArray(df_sp_prices.columns)

#SAVE TO CSV FILE
df_sp_prices.to_csv('df_sp_prices.csv', header=df_sp_prices.columns, index=True , encoding='utf-8')

print('Fetch Data Complete')
# %%
