import os
from sec_api import QueryApi
from dotenv import load_dotenv

'''
Documentation for Sec Api: https://github.com/janlukasschroeder/sec-api-python

As of now this will be where all of the Classes will be. 

The get_filings_by_stock_name function queries the sec database and returns:
|---- Documents (something called '10-Q' documents)  filtered by the stock name you provided and within a data range.

This was setup just to test the queries and the data coming from them but this is a start to query anything basically.

I provide an example of how to use the 'get_filings_by_stock_name' function in:
|----  secByStockName.py

'''

class SecData:

  # On Initilization
  def __init__(self):
    load_dotenv()
    key = os.getenv('SEC_KEY')
    self.queryApi = QueryApi(api_key=key)

  def get_filings_by_stock_name(self, stock='TSLA'):

    print(f'Querying for {stock}...', '\n')
    filedAt = '{2020-01-01 TO 2020-12-31}'

    query = {
      "query": { "query_string": {
          "query": f"ticker:{stock} AND filedAt:{filedAt} AND formType:\"10-Q\""
        } },
      "from": "0",
      "size": "10",
      "sort": [{ "filedAt": { "order": "desc" } }]
    }

    filings = self.queryApi.get_filings(query)

    count = 0


    print('Filings:', filings["total"])
    for i in filings['filings']:
      while count < len(filings['filings']):
        print(
          'Stock Namee:', filings['filings'][count]['ticker'], '\n'*2,
          'Description:', '\n', '|---', filings['filings'][count]['description'], '\n'*2,
          'Link For Filing Details:', '\n', '|---', filings['filings'][count]['linkToTxt'], '\n'*2,
          'Docs:', '\n', '|---', filings['filings'][count]['documentFormatFiles'], '\n'*2,
          )
        count += 1

