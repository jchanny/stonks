#Jeremy Chan 2020
#Class to extract todays earnings from fidelity
import requests
from datetime import datetime
from datetime import timedelta
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

#given a date formatted as "m/d/YYYY" returns earnings annountcements
#morning of and EOD yesterday
def getEarningsForDate(dt):
    tStr = datetime.strptime(dt, "%m/%d/%Y")
    tMinusOne = (tStr - timedelta(days = 1)).strftime("%m/%d/%Y")
    t = tStr.strftime("%m/%d/%Y")
    output = []
    #parse tMinusOne afternoon earnings
    data = extractStockTableForDate(tMinusOne)
    for earnings in data:
        if earnings[1] != 'Before Market': # many will be "not supplied"
            output.append(earnings)

    #this mornings earning reports
    data = extractStockTableForDate(t)
    for earnings in data:
        if earnings[1] != 'After Market':           
            output.append(earnings)

    return output


