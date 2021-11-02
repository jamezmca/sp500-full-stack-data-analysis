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

#Import from functions.py

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

# %% PART 1: FIND LOCATIONS OF NEGATIVE GRADIENT 
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

def sp500AvgPrice(werkbins, dollares):
    james = dict()
    for werk in werkbins:
        avgPrice = np.mean(np.array(dollares[int(werk.split(' ')[0]): int(werk.split(' ')[1])]) )
        james[werk] = avgPrice
    return james


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

#%%
weekBins
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
            grade = int(str(key)[:2] + '5')
            if grade not in interconnectednessHistogramSmooth:
                interconnectednessHistogramSmooth[grade] = val['list']
            else:
                interconnectednessHistogramSmooth[grade] += val['list']
    interconnectednessHistogramSmoothMetrics = {k:{'mean': np.mean(np.array(v)), 'median': np.median(np.array(v)), 'UQ': np.quantile(np.array(v), 0.75), 'LQ': np.quantile(np.array(v), 0.25), '5th': np.quantile(np.array(v), 0.05)} for k,v in interconnectednessHistogramSmooth.items()}
    interconnectednessHistogram = {k: v for k, v in sorted(interconnectednessHistogram.items(), key=lambda item: item[0])}
    interconnectednessHistogramSmoothMetrics = {k: v for k, v in sorted(interconnectednessHistogramSmoothMetrics.items(), key=lambda item: item[0])}
    return interconnectednessHistogram, interconnectednessHistogramSmooth, interconnectednessHistogramSmoothMetrics

interconnectednessHistogram, interconnectednessHistogramSmooth, interconnectednessHistogramSmoothMetrics = createInterconnectednessHistograms(weekBins)

print(f'finished part 3 for analysis finished finding {len(interconnectednessHistogramSmooth.keys())} drops')


#%% PART 4: CREATE A DICTIONARY OF EVERY MULTIPLER AND INTERCONNECTEDNESS VALUE AND RUN REGRESSION MODEL
interconnectednessReturn = dict()
for intercon, val in interconnectednessHistogramSmooth.items():
    print(intercon)
    for ret in val:
        interconnectednessReturn[ret] = intercon
interconnectednessReturn = {k: v for k, v in sorted(interconnectednessReturn.items(), key=lambda item: item[0]) if k < 2.5 and k > 0.6}

#REGRESSION ANALYSIS
eggies = [[x, w] for x,w in interconnectednessReturn.items()]

eggies_df = pd.DataFrame(eggies, columns=['Return Multiplier', 'Interconnectedness'])
eggies_df.describe()

p = np.poly1d(np.polyfit(eggies_df['Interconnectedness'], eggies_df['Return Multiplier'], 1))
regr_results = sp.stats.linregress(eggies_df['Interconnectedness'], eggies_df['Return Multiplier'])

print(f'''finished part 4 for analysis finished finding {len(interconnectednessReturn.keys())} returns. \n
The linear regression analysis found a pvalue < 0.001 which suggests statistical significance.
The gradient value from the regression analysis suggests a {regr_results.slope*100*100}% increase
in return for every 100 increase Interconnectedness and a y-intercept of {regr_results.intercept}.
''')


#%% PART 5: DETERMINE THE GREATEST RISK AND RETURN FROM EACH STOCK AND THEIR HISTORY
#GETS UPLOADED TO DB IN TABLE - 
stockReturnsList = dict()
for deep,val in negGradsForAllStocks.items():
    for hi in val.values():
        if newDict[deep] in stockReturnsList:
            stockReturnsList[newDict[deep]].append(hi['multiplier'])
        else:
            stockReturnsList[newDict[deep]] = [hi['multiplier']]

for sp500 in negGradsForSP500.values():
    if 'sp500' in stockReturnsList:
        stockReturnsList['sp500'].append(hi['multiplier'])
    else:
        stockReturnsList['sp500'] = [hi['multiplier']]

stockReturnMetricsList = dict()
for steak,val in stockReturnsList.items():
        stockReturnMetricsList[steak] = {
            'risk': len([x for x in val if x <= 1])/len(val)*100,
            'avgMultiplier': np.mean(np.array(val))
        }
# stockReturnMetricsList = {k: v for k, v in sorted(stockReturnMetricsList.items(), key=lambda item: item[1]['avgMultiplier']) if k > 0.6 and k < 2}
stockReturnMetricsList = {k: v for k, v in sorted(stockReturnMetricsList.items(), key=lambda item: item[1]['avgMultiplier'])}
stockReturn_List = [[x,v['risk'],v['avgMultiplier']] for x,v in stockReturnMetricsList.items()]
stockReturn_df = pd.DataFrame(stockReturn_List, columns=["stock", "risk", "avg_multipler"])
#Save to dataframe and to csv and create table schema
# print(stockReturnMetricsList)
# stockReturn_df = pd.DataFrame.transpose(pd.DataFrame.from_dict(stockReturnMetricsList))
stockReturn_df.to_csv('df_stock_return_risk.csv', header=stockReturn_df.columns, index=True , encoding='utf-8')
# print(pd.DataFrame.transpose(stockReturn_df))
####################TABLE SCHEMA
print('Finished risk reward csv and schema')
#%%
stockReturn_df

# %% PART 6: MOST RECENT 6 WEEKS OF STOCKS TO INITIALIZE SCANNING
#GETS UPLOADED TO DB IN TABLE - 
lastSixWeeks = df_sp_prices.tail(30)
lastFetchDate = lastSixWeeks.iloc[-1][0]

#SAVE TO CSV AND ALSO CREATE TABLE SCHEMA CSV
def arrayToString(array):
    str = ''
    for item in array:
        str += f'{item} '
    return str[:-1]
sixWeeks = {}

lastSixWeeks_list = []
for stonk,vals in lastSixWeeks.items():
    if stonk != 'Date':
        strang = arrayToString(vals)
        sixWeeks[stonk] = strang

        lastSixWeeks_list.append(
            [newDict[stonk], lastFetchDate, strang]
        )
    
print(lastFetchDate)

lastSixWeeks_df = pd.DataFrame(np.row_stack(lastSixWeeks_list), columns=['name', 'last_fetch_date', 'prices'])
lastSixWeeks_df.to_csv('df_last_six_weeks.csv', header=lastSixWeeks_df.columns, index=False , encoding='utf-8')

####################TABLE SCHEMA
print('finished making last 6 weeks csv and shema')



#%% PART 7: PLOT GRAPHS
#COMBINED GRAPH OF TOTAL DATA AND 
#PINAPPLE HAS TO BE CAREFULLY INTERPRETTED - FOR EACH BIN, I HAVE AVERAGED ALL OF THE INTERCONNECTEDNESS VALUES
pineapple = [[x, w] for x,w in returnsHistogramAverages.items()]
pineapple_df = pd.DataFrame(pineapple, columns=['Return Multiplier Bin', 'Interconnectedness Average'])
pineapple_df.describe()
fig2 = px.scatter(pineapple_df, x="Interconnectedness Average", y="Return Multiplier Bin", color="Return Multiplier Bin", template="plotly_dark")
fig2.show() #pip install kaleido
# fig2.write_image('img1.png')

cheese = [[x,v['mean']] for x,v in interconnectednessHistogramSmoothMetrics.items()]
gouda = [[x,v['LQ']] for x,v in interconnectednessHistogramSmoothMetrics.items()]
swiss = [[x,v['UQ']] for x,v in interconnectednessHistogramSmoothMetrics.items()]
cheddar = [[x,v['5th']] for x,v in interconnectednessHistogramSmoothMetrics.items()]
edam = [[x,v['median']] for x,v in interconnectednessHistogramSmoothMetrics.items()]

cheese_df = pd.DataFrame(cheese, columns=['Interconnectedness', 'Return Multiplier'])
gouda_df = pd.DataFrame(gouda, columns=['Interconnectedness', 'Return Multiplier'])
swiss_df = pd.DataFrame(swiss, columns=['Interconnectedness', 'Return Multiplier'])
cheddar_df = pd.DataFrame(cheddar, columns=['Interconnectedness', 'Return Multiplier'])
edam_df = pd.DataFrame(edam, columns=['Interconnectedness', 'Return Multiplier'])

f1 = px.line(cheese_df, x="Interconnectedness", y="Return Multiplier")
f1.update_traces(line_color='navy')
f2 = px.line(gouda_df, x="Interconnectedness", y="Return Multiplier" )
f2.update_traces(line_color='crimson')
f3 = px.line(swiss_df, x="Interconnectedness", y="Return Multiplier")
f3.update_traces(line_color='teal')
f4 = px.line(cheddar_df, x="Interconnectedness", y="Return Multiplier")
f4.update_traces(line_color='aqua')
f5 = px.line(edam_df, x="Interconnectedness", y="Return Multiplier")
f5.update_traces(line_color='purple')
f6 = px.scatter(eggies_df, x="Interconnectedness", y="Return Multiplier", color="Return Multiplier")

combined = make_subplots(x_title="Interconnectedness", y_title="Return Multiplier", )
combined.add_traces(f1.data + f2.data + f3.data + f4.data + f5.data+ f6.data)
combined.update_layout(template="plotly_dark")
combined.show()
# combined.write_image('img2.png') #pip install kaleido

#%% PART 8: CONVERT IMAGES TO BASE 64ENCODING
png_files = []
for file in os.listdir(os.getcwd()):
    if file.endswith('.png'):
        png_files.append(file)

encoded = {}
for png in png_files:
    with open(png, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        encoded[png] = encoded_string

encoded_df = pd.DataFrame(encoded.items(), columns=['png', 'code'])
encoded_df.to_csv('df_encoded.csv', header=encoded_df.columns, index=False , encoding='utf-8')

####################TABLE SCHEMA
print('finito making base64 encoded img csv and shema')

# %% PART 9(OPTIONAL): RUN THE LATEST ANALYSIS TO FIND WHICH CURRENT STOCKS ARE DOWN
storks = list()
last40Days = df_sp_prices.tail(15)
for sterk,val in last40Days.items():

    if sterk != 'Date':

        maxVal = max(val)
        minVal = min(val)
        if (not math.isnan(maxVal)) and (not math.isnan(minVal)):
            maxValIndex = list(val).index(maxVal)
            minValIndex = list(val).index(minVal)
            delta = minValIndex - maxValIndex
            if delta > 0 and maxVal / minVal > 1.15:
                print(sterk, delta, 1 - minVal / maxVal)
                storks.append(sterk)
print(storks)
# %%
