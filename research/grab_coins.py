import time
import requests
import pandas as pd
from bs4 import BeautifulSoup 
import re

def clean_name(name, symbol):
    new = name.replace(symbol, "")
    new = new.strip()
    return new

def get_coindataframe():
    URL = "https://coinmarketcap.com/all/views/all/"
    request = requests.get(URL)
    webpage = request.text
    df = pd.read_html(webpage, attrs={'id': 'currencies-all'})[0]
    df['Name'] = df.apply(lambda row: clean_name(row['Name'], row['Symbol']), axis=1)
    return df

def grab_symbols():
    df = get_coindataframe()
    symbols = df["Symbol"].tolist()
    return symbols

def grab_names():
    df = get_coindataframe()
    name = df["Name"].tolist()
    return name


if __name__ == '__main__':
    df = get_coindataframe()
    df.to_csv("coinbase_db.csv")

