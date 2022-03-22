#%% INITIALIZE
import os
import numpy as np
import pandas as pd
import scipy as sp
from scipy import stats, optimize, interpolate
import math
from datetime import date
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import base64

#%% Import from functions.py

#INITIALIZE DATAFRAMES FROM CSV FILES
df_2005 = pd.read_csv('df_2005.csv')
df_2010 = pd.read_csv('df_2010.csv')
df_2015 = pd.read_csv('df_2015.csv')
df_2021 = pd.read_csv('df_2021.csv')
print(df_2005)
dictionary = pd.read_csv('dictionary.csv')
newDict = {}
for row in dictionary.values:
    newDict[row[0]] = row[1]
print('Successfully imported csv files :)')

#REQUIRED INPUT VARIABLES
analysisRange = 0.02 #range determines allowable drop gradient
dec = 1.2 #signifies a 20 percent decrease in value
howManyDaysLater = 40 #2 month return

# %% PART 1: FIND LOCATIONS OF NEGATIVE GRADIENT 
def findLocationsOfValueDrop(df, analysisRange, decrement, how_many_days_later): #FIND ALL STATS IN HERE AND MAKE IT A BUNCH OF SMALLER FUNCTIONS AND ALSO INCLUDE WHICHEVER DATE BINS IT'S IN
    def findOverlappingWeeks(wklyBinIndexes, maxIndex, minIndex):
        maxOverlap = 0
        bongo = [] #array of bins to increment
        for key in wklyBinIndexes:
            keyStart, keyEnd =  key.split(' ')
            keyStart, keyEnd, maxIndex, minIndex = [int(keyStart), int(keyEnd), int(maxIndex), int(minIndex)]
            overlap = minIndex - keyStart if minIndex < keyEnd else keyEnd - maxIndex
            hasOverlap = (maxIndex >= keyStart and maxIndex < keyEnd) or (minIndex < keyEnd and minIndex >= keyStart)
            #if find bigger overlap, reset overlap and create for new max overlap
            if (maxIndex >= keyStart and minIndex < keyEnd) or (maxIndex <= keyStart and minIndex > keyEnd):
                overlap = 5
                bongo.append(key)
                maxOverlap = 5
            elif hasOverlap and overlap >= maxOverlap:
                maxOverlap = overlap
                bongo.append(key)
        return bongo

    def initializeWeekBins(datesArray):
        hokeyPokey = {}
        for i in range(len(datesArray)):
            if i == 0:
                hokeyPokey[f'{i} {i+5}'] = [0, {}] #dict contains stock and count of particular stock
            elif i % 5 == 0:
                hokeyPokey[f'{i} {i+5}'] = [0, {}]
        return  hokeyPokey
    week_bins = initializeWeekBins(df['Date'])

    negGradsForAllStocks = {}
    #multiplier is sufficient unique id to checo if in all bins
    foreCastHist = {'3days': {}, '6days': {}, '12days': {}, '20days': {}, 'multiplier': []} #for each forecast perctage (3days 1week etc) '3days': [[multiplier list], [list of stocks]]
    prevGradHist = {} #multiplier bins and their  {1.2: {6month: [], 3month: [], 1month: []}}
    coolBananas = [] #list of multiplers to see if it works
    for stock in df:
        if stock != 'Date' and stock != "date":
            array = df[stock]
            gradients = {}
            length = len(array)
            for i in range(length - how_many_days_later - math.floor(analysisRange*length)):
                tempArray = list(array[i:i+math.floor(analysisRange*length)])
                maximum = max(tempArray)
                maxIndex = tempArray.index(maximum) + i
                minimum = min(tempArray) if min(tempArray) != 0 else 0.001
                minIndex = tempArray.index(0) + i if minimum == 0.001 else tempArray.index(minimum) + i
                dropPercentage = maximum / minimum
                if maxIndex - minIndex != 0:
                    deltaX = maxIndex - minIndex
                else: #can just set it to a positive integer cause I only want negative gradients and max and min are the same value
                    deltaX = 15
                dateBins = findOverlappingWeeks(list(week_bins), maxIndex, minIndex)
                grad = (maximum - minimum) / deltaX #possibly should be perc/deltaX
                multiplier = array[minIndex+how_many_days_later] / minimum
                completeObj = {"max": maximum, 
                                    "min": minimum, 
                                    "grad": grad, 
                                    "dropPercen": dropPercentage,
                                    'minIndex': minIndex,
                                    'maxIndex': maxIndex,
                                    'dateBins': dateBins,
                                    'multiplier': multiplier,
                                    'stock': stock}
                if grad < 0 and dropPercentage > decrement and completeObj not in gradients.values() and completeObj['multiplier'] not in coolBananas: #ensures no double ups
                    #ANALYSIS 1 - maps neg grad properties
                    if completeObj['multiplier'] in coolBananas:
                        print('WHY ISN"T IT WORKING')
                        print(completeObj)
                    coolBananas.append(completeObj['multiplier'])
                    gradients[i] = completeObj
                    
                    #ANALYSIS 2 - gives intensity of events for a given week
                    for week in dateBins:
                        if stock not in week_bins[week][1]:
                            week_bins[week][0] += 1
                            week_bins[week][1][stock] = [multiplier]
                        else :
                            week_bins[week][1][stock].append(multiplier)
                    
                    #ANALYSIS 3 - maps 3 day val after min to it's final return
                    foreCastHist['3days'][multiplier] = array[minIndex+3] / minimum
                    foreCastHist['6days'][multiplier] = array[minIndex+6] / minimum
                    foreCastHist['12days'][multiplier] = array[minIndex+12] / minimum
                    foreCastHist['20days'][multiplier] = array[minIndex+20] / minimum
                    foreCastHist['multiplier'].append(multiplier)
            
                    #ANALYSIS 4 - maps the prior vals to a particular return
                    coeff = str(multiplier)[:3]

                    prevGradHist[multiplier] = {'1month': array[minIndex-20]/minimum if minIndex - 20 > 0 else None, 
                    '3month': array[minIndex-60]/minimum if minIndex - 60 > 0 else None, 
                    '6month': array[minIndex-120]/minimum if minIndex - 120 > 0 else None}

                    if prevGradHist[multiplier]['1month'] is not None and prevGradHist[multiplier]['1month'] > 3:
                        print('1month', stock, array[minIndex-20] ,minimum)
                    if prevGradHist[multiplier]['3month'] is not None and prevGradHist[multiplier]['3month'] > 7:
                        print('3month', stock, array[minIndex-60] ,minimum)
                    if prevGradHist[multiplier]['6month'] is not None and prevGradHist[multiplier]['6month'] > 12:
                        print('6month', stock, array[minIndex-120] ,minimum)
        
            negGradsForAllStocks[stock] = gradients
    return negGradsForAllStocks, week_bins, foreCastHist, prevGradHist

# COMPARE STOCK PRICE AVG FROM DATA SET TO STOCK PRICE FROM A YEAR AGO

yearsToWeeks = 5 * 52
xRange = yearsToWeeks * analysisRange
negGrads2021, weekBins2021, forecast2021, prevGrad2021 = findLocationsOfValueDrop(df_2021, analysisRange, dec, howManyDaysLater)
negGrads2015, weekBins2015, forecast2015, prevGrad2015 = findLocationsOfValueDrop(df_2015, analysisRange, dec, howManyDaysLater)
negGrads2010, weekBins2010, forecast2010, prevGrad2010 = findLocationsOfValueDrop(df_2010, analysisRange, dec, howManyDaysLater)
negGrads2005, weekBins2005, forecast2005, prevGrad2005 = findLocationsOfValueDrop(df_2005, analysisRange, dec, howManyDaysLater)
# print(f'The total number of negative gradient segments in the last 5 years\n of every stock in the S&P500 is: {sum} \nWith an analysis range of {xRange} weeks.')
# allStocksWeekBinsCount = {x:y[0] for x,y in weekBins.items()}

print(f'finished part 1 for analysis range: {xRange} weeks')
#%% OBJECTIVE IS TO 
forecast2021['3days']
standardVals = []
# HISTOGRAM 3 DAY RETURN BINS AND APPEND ULTIMATE MULTIPLER AND THEN RUN AVERAGEs
def forecastHisto(forecastPeriodArr):
    #takes in forecast2021['3days'] for eg
    histo = {}
    for key,val in forecastPeriodArr.items():
        simba = str(key)[:3]
        if simba in histo:
            histo[simba].append(val)
        else:
            histo[simba] = [val]

    return histo

forecastHisto2021 = forecastHisto(forecast2021['3days'])



# %%

forecastHisto2021
forecastHisto2021 = {k: v for k, v in sorted(forecastHisto2021.items(), key=lambda item: item[0])}


# %%
forecastHisto2021Filtered = {k: v for k,v in forecast2021['3days'].items() if float(k) > 1.2}
forecastHisto2021Filtered = {k: v for k, v in sorted(forecastHisto2021Filtered.items(), key=lambda item: item[0])}
# %%
forecastHisto2021Filtered
# %%
#REGRESSION ANALYSIS
eggies = [[x/w, w] for x,w in forecast2021['20days'].items()]

eggies_df = pd.DataFrame(eggies, columns=['Multiplier', 'Forecast'])
eggies_df.describe()

p = np.poly1d(np.polyfit(eggies_df['Forecast'], eggies_df['Multiplier'], 1))
regr_results = sp.stats.linregress(eggies_df['Forecast'], eggies_df['Multiplier'])

fig2 = px.scatter(eggies_df, x="Forecast", y="Multiplier", color="Multiplier", template="plotly_dark")
fig2.show() #pip install kaleido
# %%

print(p)
# %%
eggies = [[x, w['6month']] for x,w in prevGrad2005.items()]
eggies_df = pd.DataFrame(eggies, columns=['Multiplier', 'PrevGrad'])
eggies_df.describe()

# p = np.poly1d(np.polyfit(eggies_df['PrevGrad'], eggies_df['Multiplier'], 1))
regr_results = sp.stats.linregress(eggies_df['PrevGrad'], eggies_df['Multiplier'])

fig2 = px.scatter(eggies_df, x="PrevGrad", y="Multiplier", color="Multiplier", template="plotly_dark")
fig2.show() #pip install kaleido
# %%
# %%
prevGrad2010
# %%
biiiiigDrops = []
returns = []
negReturns = []
for stock in negGrads2005.values():
    for drop in stock.values():
        # print(drop)
        if drop['dropPercen'] > 1.8:
            print(drop['dropPercen'])
            returns.append(drop['multiplier'])
            biiiiigDrops.append(drop)
            if drop['multiplier'] < 1:
                negReturns.append(drop)
# %%
len(negReturns)
# %%

144/730
# %%
print(np.mean(np.array(returns)))
print(min(returns))
print(max(returns))

# %%
negReturns
# %%
filteredBD = []
for drop in biiiiigDrops:
    if drop['stock'] not in filteredBD:
        filteredBD.append(drop['stock'])

bigDrop = pd.DataFrame(biiiiigDrops)
# %%
filteredBD
# %%
