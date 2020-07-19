'''
Jeremy Chan 2020
plot trendline of option open interest
---------------------------------------
REVISION HISTORY:
  06/20 - Created
---------------------------------------
'''
import matplotlib.pyplot as plt
import math
from datetime import timedelta

'''
plot option OI @ strikes percentOTM
PARAMETERS:
   ticker: ticker
   percentOTM: percentage OTM, given as whole number
   startDate: start date, given as MM-DD-YYYY
   endDate: end date, given as MM-DD-YYYY
'''
def plotOpenInterest(auth,ticker,percentOTM,startDate,endDate):
    timeDelta = timedelta(days=1)
    startDate = datetime.strptime(startDate, '%m-%d-%y')
    endDate = datetime.strptime(endDate, '%m-%d-%y')
    putOI = []
    callOI = []
    while(startDate <= endDate):
        print startDate.strftime("%m-%d-%y")
        avgDailyPrice = ticker
        putStrike = Math.floor(avgDailyPrice * (1 - (percentOTM/100)))
        callStrike = Math.ceil(avgDailyPrice * (1 + (percentOTM/100)))
        #now plot open interest
        
        startDate += timeDelta
#---------------------------------------------------------
plotOpenInterest("SPX",5,'06-01-2020','06-20-2020')
        
    
