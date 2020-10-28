#Jeremy Chan 2020
#main entry point for scraping web data. To be called on the command line

#REVISION HISTORY
# 10/2020 - Created
from datetime import date
from datetime import timedelta
import pickle
import todays_earnings as er
import yahoo_finance_quote_scraper as yf
import pandas as pd

#returns a set of ticker names for constituents of the S&P 500 & Nasdaq 100
def getBigStonkSet():
    snp500table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df = snp500table[0]
    snp500List = df['Symbol'].tolist()
    ndq100table = pd.read_html('https://en.wikipedia.org/wiki/NASDAQ-100#Components')
    df = ndq100table[3]
    ndq100List = df['Ticker'].tolist()
    return set(snp500List + ndq100List)

#saves detailed data for companies that reported earnings this morning or yesterday afternoon
def todaysEarningsResults():
    today = date.today().strftime("%m/%d/%Y")
    earningsTable = er.getEarningsForDate(today)
    stockFilterSet = getBigStonkSet()
    if earningsTable[0][0] == '':
        return "Could not get earnings list"

    data = {}
    for earnings in earningsTable:
        ticker = earnings[0]
        if ticker in stockFilterSet:
            data[ticker] = yf.getTodaysData(ticker)

    #save to pickle 10_22_2020_earnings
    fileName = date.today().strftime("%m_%d_%Y") + "_earnings.pkl"
    output = open(fileName, "wb+") #will always create file as binary
    pickle.dump(data, output)
    output.close()

    
todaysEarningsResults()
