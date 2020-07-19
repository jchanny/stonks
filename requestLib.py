'''
Jeremy Chan 2020
Request Library for querying the TD Ameritrade API
---------------------------------------------------
REVISION HISTORY:
  06/20 - Created
---------------------------------------------------
'''
import requests
import os

def makeRequest(url,params):
    return requests.get(url,params)

OPTION_CHAIN_URL = "https://api.tdameritrade.com/v1/marketdata/chains"

'''
Returns json option data for a single option'''
def getOptionContract(ticker,strike,daysToExpiration):
    print(os.environ['tdAPIKey'])
    params = { "apiKey": os.environ['tdAPIKey'],
               "symbol": ticker,
               "strike": strike,
               "daysToExpiration": daysToExpiration
               }
    res = makeRequest(OPTION_CHAIN_URL,params)
    print(res.status_code)
   # if (res.status_code != 200):
    #    return -1
    return res.json()

print(getOptionContract('AAPL',220,0))
    
    

    
    
