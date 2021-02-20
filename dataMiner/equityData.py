'''jchan 2021

A routine to pull equity data

REVISION HISTORY
    2/21 - Initial implementation
'''
import requests 
import os
import sys
import csv

appToken = os.environ.get('TradierAppToken')
accessToken = os.environ.get('TradierAccessToken')

INTRADAY_URL = "https://sandbox.tradier.com/v1/markets/timesales"
CSV_COLUMNS = ['date','time', 'open', 'high', 'low', 'close', 'volume', 'vwap']

'''Obtain quote data between start-endDate
    @param interval: 1,5, or 15 min
    @param startDate: date in YYYY-MM-DD
    @param showMarketHoursDataOnly: False to display after hours data'''
def getStockData(ticker, startDate, endDate, interval, showMarketHoursDataOnly = True):
    if showMarketHoursDataOnly:
        startTime = "09:30"
        endTime = "16:00"
    else:
        startTime = "06:30"
        endTime = "18:59"

    if interval not in {'1min', '5min', '15min'}:
        return 

    fqStartDate = startDate + " " + startTime
    fqEndDate = endDate + " " + endTime

    headersObj = {
        'Accept' : 'application/json',
        'Authorization' : 'Bearer ' + accessToken
    }

    payload = {
        'symbol' : ticker,
        'interval' : interval,
        'start' : fqStartDate,
        'end' : fqEndDate,
        'session-filter' : ('all', 'open')[showMarketHoursDataOnly]
    }
    return requests.get(INTRADAY_URL, params = payload, headers = headersObj).json()

def writeCSV(ticker, startDate, endDate, interval = '5min', showMarketHoursDataOnly = True):
    filename = "equityData/" + ticker + startDate + "_" + endDate + ".csv"

    with open(filename, 'w', newline = '') as file:
        data = getStockData(ticker, startDate, endDate, interval, showMarketHoursDataOnly)
        writer = csv.writer(file)
        writer.writerow(CSV_COLUMNS)
        try:
            dataArr = data['series']['data']
            for dataPoint in range(len(dataArr)):
                dataRow = []
                fullDate = dataArr[dataPoint]['time']
                dataRow.append(fullDate.split("T")[0]) #date
                dataRow.append(fullDate.split("T")[1]) #time
                dataRow.append(dataArr[dataPoint]['open'])
                dataRow.append(dataArr[dataPoint]['high'])
                dataRow.append(dataArr[dataPoint]['low'])
                dataRow.append(dataArr[dataPoint]['close'])
                dataRow.append(dataArr[dataPoint]['volume'])
                dataRow.append(dataArr[dataPoint]['vwap'])
                writer.writerow(dataRow)
        except Exception:
            return

def speedScraper():
    tickerArr = []
    while True:
        ticker = input("Enter a ticker: ")
        if ticker == "":
            break
        tickerArr.append(ticker)

    startDate = input("Enter a start date as YYYY-MM-DD: ")
    endDate = input("Enter an end date as YYYY-MM-DD: ")

    if startDate = '' or endDate = '':
        return

    for i in range(len(tickerArr)):
        writeCSV(tickerArr[i], startDate, endDate, interval = '5min')
