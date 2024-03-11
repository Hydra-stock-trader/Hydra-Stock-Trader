import pandas as pd
import requests
import os
from dotenv import load_dotenv
import json


load_dotenv()

agent = os.getenv('AGENT')

headers = {'User-Agent': agent}


def getTickers():
    companyTickers = requests.get('https://www.sec.gov/files/company_tickers.json', headers=headers)
    
    tickersData = companyTickers.json()
    
    return tickersData