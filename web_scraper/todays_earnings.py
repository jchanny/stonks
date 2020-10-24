#Jeremy Chan 2020
#Class to extract todays earnings from fidelity
import requests
from bs4 import BeautifulSoup

URL_BASE = "https://eresearch.fidelity.com/eresearch/conferenceCalls.jhtml?tab=earnings&begindate="

def getEarningsHTMLForDate(date):
    return requests.get(URL_BASE + date).text

#given a date, returns list containing list objects of the form:
#[TICKER,TIME,QRTR,EPS,EST EPS,EPS DIFFERENCE,NEXT ER,NEXT ER CONFIRMED]
def extractStockTableForDate(date):
    table = []
    soup = BeautifulSoup(getEarningsHTMLForDate(date), 'lxml')
    table_body = soup.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [x.text.strip() for x in cols]
        table.append(cols)
    return table
    
def extractStockDataFromRow(htmlRow):
    return 0

print(extractStockTableForDate("10/22/2020")[0])

