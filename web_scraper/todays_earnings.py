#Jeremy Chan 2020
#Class to extract todays earnings from fidelity
import requests
from datetime import date
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
    
def extractStockDataFromRow(htmlRow):
    return

def main():
    today = date.today().strftime("%m/%d/%Y")
    yesterday = (date.today() - timedelta(days = 1)).strftime("%m/%d/%Y")
    #parse yesterday afternoon earnings
    data = extractStockTableForDate(yesterday)
    for earnings in data:
        if earnings[1] != 'After Market':
            continue


main()


