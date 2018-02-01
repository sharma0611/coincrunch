#!/usr/bin/env python3

from lib.DB import DB
from lib.exchanges import init_exchange

#metadata:
# {exchange_name: [(base_coin, quote_coin), (base_coin, quote_coin), ... ]
#  exchange_name1 : <markets>
#  ... }

class Monitor(object):
    """
    Allows us to actively monitor certain coins on exchanges & updates values to database
    """

    def __init__(self, metadata):
        self.db = DB()
        self.metadata = metadata
        #exchanges dict has {exchange_name: exchange_object}
        self.exchanges_dict = {}
        #markets dict has {exchange_name: [(basecoin_quotecoin, market_name]}
        self.markets_dict = {}

        #init all exchanges we need
        for exchange_name, markets in metadata.items():
            #init exchange & record
            exchange = init_exchange(exchange_name)
            self.exchanges_dict[exchange_name] = exchange

            #grab all the market names of markets we require
            curr_markets = []
            for market_tuple in markets:
                base_coin = market_tuple[0]
                quote_coin = market_tuple[1]
                curr_market = exchange.grab_market(base_coin, quote_coin) #this returns the market name associated with the two coins you want
                curr_markets.append(curr_market)

            #record markets for current exchange
            self.markets_dict[exchange_name] = curr_markets

            #create tables for exchange
        for name in market_names:
            self.cur.execute("CREATE TABLE IF NOT EXISTS " + name + "(datestamp DATETIME, ask REAL, bid REAL)")
            self.conn.commit()


    def push_askbid(self, timestamp, askbid_dict):
        for name in market_names: 
            (lowest_ask, highest_bid) = (askbid_dict[name]['ask'], askbid_dict[name]['bid'])
            insert_query = "INSERT INTO " + name + " values ({0}, {1}, {2})".format(timestamp, lowest_ask, highest_bid)
            self.cur.execute(insert_query)
            self.conn.commit()

    def begin_stream(self, verbose=False):
        try:
            while(True):
                ts, askbid = self.cb.grab_basecoins_askbid()
                ts = ts.strftime(strtime)
                if verbose:
                    print(askbid)
                self.push_askbid(ts, askbid)
                time.sleep(3)
        finally:
            self.db.close_db()




        #begin connection with coinbase
        cb = exch.Coinbase()
        self.cb = cb
