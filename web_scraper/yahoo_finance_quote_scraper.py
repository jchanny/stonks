#Jeremy Chan 2020
#Scraper for scraping data off yahoo finance
import json
import requests
import re
from bs4 import BeautifulSoup

URL_BASE = "https://finance.yahoo.com/quote/"

#-------------------------------------------
#JSON manipulation methods
#-------------------------------------------

def getQuoteSummaryStore(jsonDump):
    return jsonDump['context']['dispatcher']['stores']['QuoteSummaryStore']

def getResearchStore(jsonDump):
    return jsonDump['context']['dispatcher']['stores']['ResearchPageStore']

#returns [technicalInsights][ticker]
def getTechnicalInsights(jsonDump):
    rsrchStore = getResearchStore(jsonDump)
    ticker = list(rsrchStore['technicalInsights'].keys())[0]
    return rsrchStore['technicalInsights'][ticker]
    
#-------------------------------------------
#data retrieval methods
#-------------------------------------------

#returns technical info summary 
def getTechnicalSummary(jsonDump):
    output = {}
    filteredData = getTechnicalInsights(jsonDump)
    output['company'] = filteredData['companySnapshot']['company']
    output['outlook'] = filteredData['instrumentInfo']['technicalEvents']['shortTermOutlook']
    output['technicals'] = filteredData['instrumentInfo']['keyTechnicals']
    output['valuation'] = filteredData['instrumentInfo']['valuation']
    output['technicalTrend'] = filteredData['events']
    output['targetPrice'] = filteredData['recommendation']
    return output;

#returns fundamental data 
def getFundamentalsSummary(jsonDump):
    output = {}
    quoteStore = getQuoteSummaryStore(jsonDump)
    output['analystTrend'] = quoteStore['recommendationTrend']

    priceMeasures = {}
    for measure in quoteStore['price']:
        if quoteStore['price'][measure]:
           priceMeasures[measure] = quoteStore['price'][measure]
           
    output['price'] = priceMeasures
    fundamentalStats = {}
    
    for stat in quoteStore['defaultKeyStatistics']:
        if quoteStore['defaultKeyStatistics'][stat]:
            fundamentalStats[stat] = quoteStore['defaultKeyStatistics'][stat]
    for stat in quoteStore['financialData']:
        if quoteStore['financialData'][stat]:
            fundamentalStats[stat] = quoteStore['financialData'][stat]

    output['fundamentals'] = fundamentalStats
    return output

#------------------------------------------
#main methods
#------------------------------------------
#kills off some subscripts to minimize the JSON dump    
def cleanUpJSON(jsonDump):
    del jsonDump['context']['dispatcher']['stores']['PageStore']
    del jsonDump['context']['dispatcher']['stores']['MRTStore']
    del jsonDump['context']['dispatcher']['stores']['RouteStore']
    del jsonDump['context']['dispatcher']['stores']['I13nStore']
    del jsonDump['context']['dispatcher']['stores']['PageTransitionStore']
    del jsonDump['context']['dispatcher']['stores']['VideoPlayerStore']
    del jsonDump['context']['dispatcher']['stores']['QuoteAutoCompleteStore']
    del jsonDump['context']['dispatcher']['stores']['FlyoutStore']
    del jsonDump['context']['dispatcher']['stores']['NavrailStore']
    del jsonDump['context']['dispatcher']['stores']['StreamDataStore']
    del jsonDump['context']['dispatcher']['stores']['FinanceConfigStore']
    del jsonDump['context']['dispatcher']['stores']['LangStore']
    del jsonDump['context']['dispatcher']['stores']['BeaconStore']
    del jsonDump['context']['dispatcher']['stores']['AdStore']
    del jsonDump['context']['dispatcher']['stores']['VideoStore']
    del jsonDump['context']['dispatcher']['stores']['ComponentConfigStore']
    del jsonDump['context']['dispatcher']['stores']['CrumbStore']
    del jsonDump['context']['dispatcher']['stores']['CompositeStore']
    del jsonDump['context']['dispatcher']['stores']['StreamStore']
    del jsonDump['context']['dispatcher']['stores']['UserStore']
    del jsonDump['context']['dispatcher']['stores']['ProfileStore']
    del jsonDump['context']['dispatcher']['stores']['QuotePageStore']
    del jsonDump['context']['dispatcher']['stores']['NavServiceStore']
    del jsonDump['context']['dispatcher']['stores']['MarketSummaryStore']
    del jsonDump['context']['dispatcher']['stores']['MarketTimeStore']
    del jsonDump['context']['dispatcher']['stores']['UHAccountSwitchStore']
    del jsonDump['context']['dispatcher']['stores']['RecommendationStore']
    del jsonDump['context']['dispatcher']['stores']['MobileHeaderStore']
    return jsonDump
    
    
#returns the JSON data dump for a given ticker, this is raw dog
def getJSONDataDump(ticker):
    soup = BeautifulSoup(requests.get(URL_BASE + ticker).text, 'lxml')
    pattern = re.compile('root.App.main')
    res = str(soup.find_all('script',text = pattern))
    jsonStr = res.split('\n')[5].split(' = ')[1][:-1]
    return json.loads(jsonStr)

#main entry point. given ticker, gib json dump
def getTodaysData(ticker):
    jsonDump = cleanUpJSON(getJSONDataDump(ticker))
    print(getFundamentalsSummary(jsonDump))
    
    
getTodaysData("CRM")
