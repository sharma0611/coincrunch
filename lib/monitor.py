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

        #init all exchanges we need
        for exchange_name, markets in metadata.items():
            #init exchange & record
            print("Initializing exchange: " + str(exchange_name))
            exchange = init_exchange(exchange_name)
            self.exchanges_dict[exchange_name] = exchange

            #create tables for exchange
            self.db.execute("CREATE TABLE IF NOT EXISTS " + exchange_name + "(datestamp TIMESTAMP, ask REAL, bid REAL, market VARCHAR(14), market_sym VARCHAR(14))") #hard code what columns we want to record

    #update database for each exchange & market 
    def update_data(self):
        # for each exchange
        for exch_name, exch_obj in self.exchanges_dict.items():
            # for each market
            curr_markets = self.metadata[exch_name]
            for market in curr_markets:
                base_coin = market[0]
                quote_coin = market[1]
                curr_data = exch_obj.grab_data(base_coin, quote_coin)
                insert_query = "INSERT INTO " + exch_name + " values ({0}, {1}, {2}, {3})".format(*curr_data)
                self.db.execute(insert_query)

#    def push_askbid(self, timestamp, askbid_dict):
#        for name in market_names: 
#            (lowest_ask, highest_bid) = (askbid_dict[name]['ask'], askbid_dict[name]['bid'])
#            insert_query = "INSERT INTO " + name + " values ({0}, {1}, {2})".format(timestamp, lowest_ask, highest_bid)
#            self.cur.execute(insert_query)
#            self.conn.commit()
#
#    def begin_stream(self, verbose=False):
#        try:
#            while(True):
#                ts, askbid = self.cb.grab_basecoins_askbid()
#                ts = ts.strftime(strtime)
#                if verbose:
#                    print(askbid)
#                self.push_askbid(ts, askbid)
#                time.sleep(3)
#        finally:
#            self.db.close_db()
#
#
#
#
#        #begin connection with coinbase
#        cb = exch.Coinbase()
#        self.cb = cb
