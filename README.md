# stonks
various stonk analysis tools:

v1: Web scraper scrapes and dumps pickle'd data into an S3 data lake (maybe a data swamp?). Do something with the data.
v2: Create a service to query the data lake 

The web_scraper folder:
  - scraper.py: main entry point that will get data for S&P500 + Nasdaq 100 stocks that reported at market close yesterday or today before market open and save it to a pickle.
  Intended to be hosted on an EC2 instance that pipes data to an S3 instance.
  - todays_earnings.py: routine that gets a list of tickers that reported earnings either today before market open or yesterday after market close
  - yahoo_finance_quote_scraper.py: routine that gets a snapshot of a ticker's financial data from yahoo finance
