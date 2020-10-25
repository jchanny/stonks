#Jeremy Chan 2020
#main entry point for scraping web data. To be called on the command line

#REVISION HISTORY
# 10/2020 - Created

import todays_earnings as er
import yahoo_finance_quote_scaper as yf

def getEarningsDataForDate(date):
    earningsTable = er.extractStockTableForDate(date)
    data = {}
    
    for earnings in earningsTable:
        ticker = earnings[0]
        data[ticker] = getTodaysData(ticker)
        
