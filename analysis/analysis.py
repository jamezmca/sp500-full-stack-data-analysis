#%% INITIALIZE
# import os
import numpy as np
import pandas as pd
import scipy as sp
from scipy import stats, optimize, interpolate
import math
from datetime import date
import plotly.express as px
from plotly.subplots import make_subplots

#Import from functions.py
from functions import initializeWeekBins, findLocationsOfValueDrop, findOverlappingWeeks, sp500AvgPrice

#INITIALIZE DATAFRAMES FROM CSV FILES
df_sp_prices = pd.read_csv('df_sp_prices.csv')
df_sp_price = pd.read_csv('df_sp_price.csv')
dictionary = pd.read_csv('dictionary.csv')
dates = df_sp_prices['Date']
newDict = {}
for row in dictionary.values:
    newDict[row[0]] = row[1]
print('Successfully imported csv files :)')

#REQUIRED INPUT VARIABLES
analysisRange = 0.01 #range determines allowable drop gradient
dec = 1.2 #signifies a 20 percent decrease in value
howManyDaysLater = 60 #2 month return

#FUNCTIONS
def initializeWeekBins(datesArray):
    hokeyPokey = {}
    for i in range(len(datesArray)):
        if i == 0:
            hokeyPokey[f'{i} {i+5}'] = [0, {}] #dict contains stock and count of particular stock
        elif i % 5 == 0:
            hokeyPokey[f'{i} {i+5}'] = [0, {}]
    return  hokeyPokey

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

def sp500AvgPrice(werkbins, dollares):
    james = dict()
    for werk in werkbins:
        avgPrice = np.mean(np.array(dollares[int(werk.split(' ')[0]): int(werk.split(' ')[1])]) )
        james[werk] = avgPrice
    return james

def findLocationsOfValueDrop(array, analysisRange, decrement, stack, how_many_days_later, week_bins): #FIND ALL STATS IN HERE AND MAKE IT A BUNCH OF SMALLER FUNCTIONS AND ALSO INCLUDE WHICHEVER DATE BINS IT'S IN
    gradients = {}
    length = len(array)
    for i in range(length - how_many_days_later - math.floor(analysisRange*length)):
        tempArray = list(array[i:i+math.floor(analysisRange*length)])
        maximum = max(tempArray)
        maxIndex = tempArray.index(maximum) + i
        minimum = min(tempArray) if min(tempArray) != 0 else 0.001
        minIndex = tempArray.index(0) + i if minimum == 0.001 else tempArray.index(minimum) + i
        decreaseRatio = maximum / minimum
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
                            "decreaseRatio": decreaseRatio,
                            'minIndex': minIndex,
                            'maxIndex': maxIndex,
                            'dateBins': dateBins,
                            'multiplier': multiplier}
        if grad < 0 and decreaseRatio > decrement and completeObj not in gradients.values(): #ensures no double ups
            gradients[i] = completeObj
            for week in dateBins:
                if stack not in week_bins[week][1]:
                    week_bins[week][0] += 1
                    week_bins[week][1][stack] = multiplier
                elif multiplier > week_bins[week][1][stack]:
                    week_bins[week][1][stack] = multiplier
    return gradients, week_bins


def createInterconnectednessHistograms(veekbins):
    interconnectednessHistogram = dict()

    for wek in veekbins.values():
        interCon = wek[0]
        if interCon in interconnectednessHistogram:
            interconnectednessHistogram[interCon]['list'] += (list(wek[1].values())) 
            listItems = np.array(interconnectednessHistogram[interCon]['list'])
            interconnectednessHistogram[interCon]['listLength'] = len(listItems)
            interconnectednessHistogram[interCon]['mean'] = np.mean(np.array(listItems))
            interconnectednessHistogram[interCon]['median'] = np.median(np.array(listItems))
            interconnectednessHistogram[interCon]['LQ'] = np.quantile(np.array(listItems), 0.25)
            interconnectednessHistogram[interCon]['UQ'] = np.quantile(np.array(listItems), 0.75)
            interconnectednessHistogram[interCon]['5th'] = np.quantile(np.array(listItems), 0.05)
        else:
            listItems = list(wek[1].values())
            if len(listItems) > 0:
                npyarray = np.array(listItems)
                interconnectednessHistogram[interCon] = {
                    'list': listItems,
                    'listLength': len(listItems), 
                    'mean': np.mean(npyarray),
                    'median': np.median(npyarray),
                    'LQ': np.quantile(npyarray, 0.25),
                    'UQ': np.quantile(npyarray, 0.75),
                    '5th': np.quantile(npyarray, 0.05)
                }
                
    #MAYBE MAKE SEPARATE ARRAYS AND PROCESS USING DICTIONARY COMPREHENSION AND SEPARATE INTO HISTOGRAM BINS OF INCREMENT 10
    interconnectednessHistogramSmooth = dict()
    for key,val in interconnectednessHistogram.items():
        if key < 100:
            grade = int(str(key)[:1] + '5') #BIN DETERMINANT
            if key < 10:
                if 5 not in interconnectednessHistogramSmooth:
                    interconnectednessHistogramSmooth[5] = val['list']
                else: 
                    interconnectednessHistogramSmooth[5] += val['list']
            else:
                if grade not in interconnectednessHistogramSmooth:
                    interconnectednessHistogramSmooth[grade] = val['list']
                else:
                    interconnectednessHistogramSmooth[grade] += val['list']
        else : 
            grade = int(str(key)[:1] + '05')
            if grade not in interconnectednessHistogramSmooth:
                interconnectednessHistogramSmooth[grade] = val['list']
            else:
                interconnectednessHistogramSmooth[grade] += val['list']
    interconnectednessHistogramSmoothMetrics = {k:{'mean': np.mean(np.array(v)), 'median': np.median(np.array(v)), 'UQ': np.quantile(np.array(v), 0.75), 'LQ': np.quantile(np.array(v), 0.25), '5th': np.quantile(np.array(v), 0.05)} for k,v in interconnectednessHistogramSmooth.items()}


    interconnectednessHistogram = {k: v for k, v in sorted(interconnectednessHistogram.items(), key=lambda item: item[0])}
    interconnectednessHistogramSmoothMetrics = {k: v for k, v in sorted(interconnectednessHistogramSmoothMetrics.items(), key=lambda item: item[0])}

    return interconnectednessHistogram, interconnectednessHistogramSmooth, interconnectednessHistogramSmoothMetrics

# %% PART 1: FIND LOCATIONS OF NEGATIVE GRADIENT 
yearsToWeeks = 5 * 52
xRange = yearsToWeeks * analysisRange

weekBins = initializeWeekBins(dates)
negGradsForAllStocks = {}
for stock in df_sp_prices:
    if stock != 'date' and stock != 'Date':
        negGradsForAllStocks[stock], weekBins = findLocationsOfValueDrop(df_sp_prices[stock], analysisRange, dec, stock, howManyDaysLater, weekBins)
# print(f'The total number of negative gradient segments in the last 5 years\n of every stock in the S&P500 is: {sum} \nWith an analysis range of {xRange} weeks.')
allStocksWeekBinsCount = {x:y[0] for x,y in weekBins.items()}

spWkBins = initializeWeekBins(dates)
negGradsForSP500, spWkBins = findLocationsOfValueDrop(df_sp_price['price'], analysisRange, dec, 'S&P500', howManyDaysLater, spWkBins)
spAvgPricePerWkBin = sp500AvgPrice(spWkBins, df_sp_price['price'])

print(f'finished part 1 for analysis range: {xRange} weeks')

#%% PART 2: CREATE HISTOGRAM OF RETURN MULTIPLIER AND AVERAGE INTERCONNECTEDNESS FROM LIST OF ASSOCIATES INTERCONNECTEDNESSES

returnsHistogramLists = dict()

for welk in  weekBins.values():
    for k,v in welk[1].items():
        grade = np.around(v, 1)
        if grade in returnsHistogramLists:
            returnsHistogramLists[grade].append(welk[0])
        else:
            returnsHistogramLists[grade] = [welk[0]]
returnsHistogramLists = {k: v for k, v in sorted(returnsHistogramLists.items(), key=lambda item: item[0]) if k > 0.6 and k < 2}
returnsHistogramAverages = {k:np.mean(np.array(v)) for k,v in returnsHistogramLists.items()}

print(f'finished part 2 for analysis finished')

#%% PART 3: CREATE THE INVERSE OF THE ABOVE SO PERCENTILES FOR AN INTERCONNECTEDNESS AND PERCENTILES OF THE RETURN VALUE LIST

interconnectednessHistogram, interconnectednessHistogramSmooth, interconnectednessHistogramSmoothMetrics = createInterconnectednessHistograms(weekBins)

print(f'finished part 2 for analysis finished finding {len(interconnectednessHistogramSmooth.keys())} drops')
# %%

# %%
