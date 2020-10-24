#Jeremy Chan 2020
#Scraper for scraping data off yahoo finance
import json
import requests
import re
from bs4 import BeautifulSoup

URL_BASE = "https://finance.yahoo.com/quote/"

def getJSONDataDump(ticker):
    soup = BeautifulSoup(requests.get(URL_BASE + ticker).text)
    pattern = re.compile('root.App.main')
    res = str(soup.find_all('script',text = pattern))
    jsonStr = res.split('\n')[5].split(' = ')[1][:-1]
    return json.loads(jsonStr)
    
print(getJSONDataDump("CRM"))
    
