#Jeremy Chan 2020
#main entry point for scraping web data. To be called on the command line

#REVISION HISTORY
# 10/2020 - Created
from datetime import date
from datetime import timedelta
import todays_earnings as er
import yahoo_finance_quote_scraper as yf

def todaysEarningsResults():
   # today = date.today().strftime("%m/%d/%Y")
    today = date.today()
    today = (today - timedelta(days = 4)).strftime("%m/%d/%Y")
    earningsTable = er.getEarningsForDate(today)
    if earningsTable[0][0] == '':
        return "Could not get earnings list"

    data = {}
    for earnings in earningsTable:
        ticker = earnings[0]
        data[ticker] = yf.getTodaysData(ticker)

    return data       
        
print(todaysEarningsResults())
