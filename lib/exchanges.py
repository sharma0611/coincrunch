import ccxt
from datetime import datetime
import os.path

basecoin_fp = './basecoindata.db'
basecoins = ['BTC','LTC','ETH']
quotecoin = 'USD'
max_latency = 5 
strtime = "%Y-%m-%d-%M-%S"
markets = [bc + "/" + quotecoin for bc in basecoins]
market_names = [bc + "_" + quotecoin for bc in basecoins]


#defining exchange class
class Exchange(object):
    """
    An exchange object holds an exchange & its markets
    """
    def __init__(self, exchange_name):
        self.exchange_name = exchange_name
 
# Define subclasses of exchanges
class Coinbase(Exchange):
    """
    Holds the Coinbase Exchange
    """
    def __init__(self):
        Exchange.__init__(self, "Coinbase")
        exch = ccxt.gdax()
        exch.load_markets()
        self.exch = exch
    
    def grab_basecoins_askbid(self):
        """ returns datestamp and dict of basecoins as keys, array of [ask, bid] as dict """ 
        start = datetime.now()
        askbid_dict = {}
        exch = self.exch
        for idx, mkt in enumerate(markets):
            order_book = exch.fetch_order_book(mkt)
            asks = order_book['asks']
            bids = order_book['bids']
            lowest_ask = asks[0][0]
            highest_bid = bids[0][0]
            curr_askbid = {'ask': lowest_ask,
                           'bid': highest_bid}
            askbid_dict[market_names[idx]] = curr_askbid

        end = datetime.now()
        latency = (end - start).seconds
        assert latency < max_latency
        return start, askbid_dict
