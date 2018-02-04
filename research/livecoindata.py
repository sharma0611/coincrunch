#!/usr/bin/env python3

import ccxt
import time

def grab_all_exchanges():
    exchanges = ccxt.exchanges
    exchanges = [exch.strip() for exch in exchanges]
    print("Number of Exchanges:")
    print(len(exchanges))

    #dict of exchanges & names
    markets_dict = {}

    #array of exchange objects
    exchange_objs = []

    for exch in exchanges:
        #print("Current Exchange: " + exch)
        try:
            exec(exch + " = ccxt." + exch + "()")
            exec("exchange_objs.append(" + exch + ")")
            exec("curr_mkts = " + exch + ".load_markets()")
            exec("markets_dict['" + exch + "'] = curr_mkts.keys()")
            #exec("print(curr_mkts.keys())")
        except:
            pass

    return markets_dict




"""

coinmate = ccxt.coinmate()
coinmate.load_markets()
coinmate_mkt = coinmate.markets
coinmate_keys = coinmate_mkt.keys()
print("coinmate markets:") 
print(len(coinmate_keys))
print(coinmate_keys)

poloniex = ccxt.poloniex()
poloniex.load_markets()
poloniex_mkt = poloniex.markets
poloniex_keys = poloniex_mkt.keys()
print("poloniex markets:") 
print(len(poloniex_keys))
print(poloniex_keys)

coinmate_symbols = coinmate_mkt.keys()
poloniex_symbols = poloniex_mkt.keys()
print("in both:")
intersect = set(coinmate_symbols).intersection(poloniex_symbols)
print(len(intersect))
print(intersect)


coinmarketcap = ccxt.coinmarketcap()
coinmarketcap.load_markets()
coinmarketcap_mkt = coinmarketcap.markets
coinmarketcap_keys = coinmarketcap_mkt.keys()
print("coinmarketcap markets:") 
print(len(coinmarketcap_keys))
print(coinmarketcap_keys)
coinmarketcap_symbols = coinmarketcap_mkt.keys()
print("in both:")
intersect = set(coinmarketcap_symbols).intersection(poloniex_symbols)
print(len(intersect))
print(intersect)

for symbol in coinmarketcap.markets:
    print(symbol)
    print(coinmarketcap.fetch_order_book(symbol))
    time.sleep(1)
"""


#function that cleans all keys to be base/quote format
def clean_markets(markets):
    clean_markets={}
    for mkt, mkt_data in markets.items():
        base = mkt_data['base']
        quote = mkt_data['quote']
        clean_markets[base + '/' + quote] = mkt_data
    return clean_markets

