#!/usr/bin/env python3

from lib.db import DB
from lib.exchanges import init_exchange
from lib.multithread import run_methods_parallel
import time
import traceback
from datetime import datetime

#metadata:
# {exchange_name: [(base_coin, quote_coin), (base_coin, quote_coin), ... ]
#  exchange_name1 : <markets>
#  ... }

#max number of tries 
max_tries = 5

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

    #stage changes to DB; commit occurs in update_data
    def update_data_exchanges(self, exch_name, exch_obj, exch_markets):
        # for each market
        temp_store = []
        for market in exch_markets:
            base_coin = market[0]
            quote_coin = market[1]
            curr_tries = 1
            while (curr_tries <= max_tries):
                try:
                    curr_data = exch_obj.grab_data(base_coin, quote_coin)
                    break
                except Exception as e:
                    curr_tries += 1
                    print("Failed to grab data for " + str(exch_name) + " " + str(market) + ". Error: " + str(e))
                    print(traceback.format_exc())
                    print("Attempt #: " + str(curr_tries))
            temp_store.append((exch_name, curr_data))
        return temp_store

    def post_data(self, temp_store):
        now = datetime.now()
        print(len(temp_store))
        print(temp_store)
        for exch_name, curr_data in temp_store:
            insert_query = "INSERT INTO " + exch_name + " values ('{0}', {1}, {2}, '{3}', '{4}')".format(*curr_data)
            self.db.execute(insert_query)
        self.db.commit()
        end = datetime.now()
        print("Updated DB in " + str((end-now).total_seconds()) + " s." )


    #update database for each exchange & market 
    def update_data(self):
        total_markets = 0
        # for each exchange
        # create methods dict to run in parallel
        methods_arr = []
        for exch_name, exch_obj in self.exchanges_dict.items():
            curr_markets = self.metadata[exch_name]
            methods_arr.append([self.update_data_exchanges, exch_name, exch_obj, curr_markets])
            total_markets += len(curr_markets)
        #run all exchanges in parrallel
        temp_store = run_methods_parallel(methods_arr)
        #push data in temp store to database
        self.post_data(temp_store)
        return total_markets

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
