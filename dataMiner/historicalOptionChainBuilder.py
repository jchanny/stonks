'''jchan 2021
Program to Build a historical options chain from a quote

REVISION HISTORY:
    2/21 - v1 implementation
'''
import os
import datetime
import requests
import time
import tokens as tokens

from datetime import date

appToken = tokens.TradierAppToken
accessToken = tokens.TradierAccessToken

HISTORICAL = "https://sandbox.tradier.com/v1/markets/history"
OPTION_SYMBOLS = "https://sandbox.tradier.com/v1/markets/options/lookup"


'''---------------------------------------------------------
                       UTILITIES
------------------------------------------------------------'''
#returns a STRING, not a datetime
def get3rdFriday(year,month):
    halfMonth = datetime.date(year, month, 15)
    halfMonthDay = halfMonth.weekday()
    if halfMonthDay != 4:
        return halfMonth.replace(day=(15 + (4 - halfMonthDay) % 7)).strftime('%Y-%m-%d')
    return halfMonth.strftime('%Y-%m-%d')

#returns a STRING, not a datetime
def get3rdFridayNextMonth():
    today = date.today().strftime('%Y-%m-%d')
    split = today.split('-')
    year = int(split[0])
    month = (int(split[1]) + 1) % 12
    return get3rdFriday(year,month)

def optionRootSymbol(json):
    return json['symbols'][0]['rootSymbol']

def optionContracts(json):
    return json['symbols'][0]['options']

def extractStrikeFromContract(contract,ticker):
    strike = contract[len(ticker) + 6 :]
    return int(int(strike) / 1000)

def filterContractsByExpiration(json, expiration):
    tickerLen = len(optionRootSymbol(json))
    contracts = optionContracts(json)
    yy = expiration[2:4]
    mm = expiration[5:7]
    dd = expiration[8:10]
    dateStr = yy + mm + dd
    valid = []
    for contract in contracts:
        if contract[tickerLen : tickerLen + 6] == dateStr:
            valid.append(contract)
    return valid

'''returns the top x strikes in both directions'''
def filterContractsByStrike(contracts, strikes, ticker, targetPrice):
    strikesSet = set()
    
    for option in contracts:
        strikesSet.add(extractStrikeFromContract(option, ticker))

    strikesList = []
    for strike in strikesSet:
        strikesList.append(strike)
    strikesList.sort()
    
    atmIdx = strikesList.index(getAtMoneyPrice(targetPrice, strikesList))
    if int(len(strikesList) / 2) <= strikes:
        return contracts
    
    #generate set of strikes to pull
    leftPtr = atmIdx - 1
    rightPtr = atmIdx + 1
    validStrikes = set()
    validStrikes.add(strikesList[atmIdx])
    for i in range(strikes):
        validStrikes.add(strikesList[leftPtr])
        validStrikes.add(strikesList[rightPtr])
        leftPtr = leftPtr - 1
        rightPtr = rightPtr + 1
    
    #now actually get the contracts that match the strike
    output = []
    for contract in contracts:
        if extractStrikeFromContract(contract, ticker) in validStrikes: 
            output.append(contract)
    
    return output

def getAtMoneyPrice(atMoneyPrice, strikeList):
    #binary search to see if we can find the closest strike below strikePrice
    left = 0
    right = len(strikeList) - 1
    while(left <= right):
        mid = int((right + left) / 2) 
        if strikeList[mid] == atMoneyPrice:
            return strikeList[mid]
        if strikeList[mid] > atMoneyPrice:
            right = mid - 1
        else:
            left = mid + 1
    if mid > 0 and abs(strikeList[mid - 1] - atMoneyPrice) <= abs(strikeList[mid] - atMoneyPrice):
        return strikeList[mid - 1]
    return strikeList[mid]


'''--------------------------------------------------------
       API Calls
-----------------------------------------------------------'''
'''
Finds all available unexpired strikes for a symbol'''
def getOptionContracts(symbol):
    headersObj = {
        'Accept' : 'application/json',
        'Authorization' : 'Bearer ' + accessToken
    } 
    payload = {
        'underlying' : symbol
    }
    return requests.get(OPTION_SYMBOLS, params = payload, headers = headersObj).json()

def getHistoricalData(contract, start, end):
    payload = {
        'symbol' : contract,
        'interval' : 'daily',
        'start' : start,
        'end' : end
    }
    headersObj = {
        'Authorization' : 'Bearer ' + accessToken,
        'Accept' : 'application/json'
    }
    return requests.get(HISTORICAL, params = payload, headers = headersObj).json()

'''------------------------------------------------------
       Main methods
--------------------------------------------------------'''

''' @param symbol: stock ticker
    @param days: days from today to go back (note days, not trading days)
    @param maxStrikes: max number of strikes in each direction to return, default is 25
    @returns: json object with historical options chain for options that haven't expired yet
    '''
def getHistoricalChain1MonthOut(symbol, days, maxStrikes = 25):
    expDate = get3rdFridayNextMonth()
    options = filterContractsByExpiration(getOptionContracts(symbol), expDate)
    start = (datetime.datetime.now() - datetime.timedelta(30)).strftime('%Y-%m-%d')
    end = (datetime.datetime.now()).strftime('%Y-%m-%d')

    data = {}
    batchCount = 1
    for option in options:
        if batchCount > 59 : #rate limiting is 60
            time.sleep(60)
            batchCount = 0
        data[option] = getHistoricalData(option, start, end)['history']['day']
        batchCount = batchCount + 1
    return data

def getHistoricalChain(symbol, start, end, maxStrikes = 25):
    #calculate all expirations between start + end

