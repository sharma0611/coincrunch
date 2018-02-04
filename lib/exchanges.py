#!/usr/bin/env python3
import ccxt
from datetime import datetime
import os.path
import cfscrape

basecoin_fp = './basecoindata.db'
basecoins = ['BTC','LTC','ETH']
quotecoin = 'USD'
max_latency = 10
strtime = "%Y-%m-%d %H:%M:%S"
markets = [bc + "/" + quotecoin for bc in basecoins]
market_names = [bc + "_" + quotecoin for bc in basecoins]

def init_exchange(exch_name):
    if exch_name == "gdax":
        return Coinbase()
    if exch_name == "bitfinex":
        return Bitfinex()
    else:
        exch = Exchange(exch_name)
        exch.init_exchange()
        return exch
        

#defining exchange class
class Exchange(object):
    """
    An exchange object holds an exchange & its markets
    """
    def __init__(self, exchange_name):
        self.exchange_name = exchange_name

    #use if you want to initialize exchange with default attributes
    def init_exchange(self):
        exch = getattr(ccxt, self.exchange_name)({
            'timeout': 20000,
            'session': cfscrape.create_scraper(),
            'enableRateLimit': True,
        })
        exch.load_markets()
        self.exch = exch

    def grab_market(self, basecoin, quotecoin):
        default_market = basecoin + "/" + quotecoin
        return default_market

    #should return: [timestamp, ask, bid, market_name, market_sym] 
    def grab_data(self, basecoin, quotecoin):
        start = datetime.now()
        market_sym = self.grab_market(basecoin, quotecoin)
        curr_data = self.grab_market_data(market_sym)
        end = datetime.now()
        latency = (end - start).seconds
        if not latency < max_latency:
            print("Warning: breached max latency on data pull")
        return [start.strftime(strtime)] + curr_data + [basecoin + "/" + quotecoin, market_sym]

    #we need to implement specific of what data to return in this fn:
    #should return: [ask, bid]
    def grab_market_data(self, market_sym):
        exch = self.exch
        order_book = exch.fetch_order_book(market_sym)
        asks = order_book['asks']
        bids = order_book['bids']
        try:
            lowest_ask = asks[0][0]
            highest_bid = bids[0][0]
        except IndexError as e:
            print("bid or ask data not available currently for " + str(market_sym))
            lowest_ask = None
            highest_bid = None
            raise e
        return [lowest_ask, highest_bid]
 
# Define subclasses of exchanges
class Coinbase(Exchange):
    """
    Holds the Coinbase Exchange
    """
    def __init__(self):
        Exchange.__init__(self, "Coinbase")
        exch = getattr(ccxt, "gdax")({
            'timeout': 20000,
            'session': cfscrape.create_scraper(),
            'enableRateLimit': True,
        })
        exch.load_markets()
        self.exch = exch

# Define subclasses of exchanges
class Bitfinex(Exchange):
    """
    Holds the Coinbase Exchange
    """
    def __init__(self):
        Exchange.__init__(self, "Coinbase")
        exch = getattr(ccxt, "bitfinex")({
            'timeout': 20000,
            'session': cfscrape.create_scraper(),
            'enableRateLimit': True,
            'rateLimit': 2500
        })
        exch.load_markets()
        self.exch = exch
