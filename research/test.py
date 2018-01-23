import ccxt
from grab_coins import grab_symbols

basecoins = ['BTC','LTC','ETH', 'CAD']
quotecoin = 'USD'
all_bases = basecoins + [quotecoin]
max_latency = 5 
strtime = "%Y-%m-%d-%M-%S"

#create all possible markets we want to look at
all_markets = []
symbols = grab_symbols()
for bc in all_bases:
    for symbol in symbols:
        curr = symbol + "/" + bc
        all_markets.append(curr)

#connect to exchanges
exchanges = ccxt.exchanges
exch_objs = []
for exch in exchanges:
    exec(exch + " = ccxt." + exch + "()")
    exec("exch_objs.append(" + exch + ")")

#take each exchange symbols and match them with ours; putting matches in a dictionary
match_dict = {}
currencies = []
for exch in exch_objs:
    curr_exch = exch.id
    curr_symbols = exch.symbols
    try:
        matching_symbols = set(curr_symbols).intersection(all_markets)
        if len(matching_symbols) > 0:
            currencies = currencies + list(matching_symbols)
            match_dict[curr_exch] = list(matching_symbols)
    except:
        pass
currencies = set(currencies) 
print(len(currencies))
print(currencies)
print(len(match_dict))
print(match_dict)

