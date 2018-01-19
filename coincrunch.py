
import ccxt
import pandas
import sqlite3
import os.path
from datetime import datetime 
import time

import matplotlib.pyplot as plt
import numpy as np
from common.exchanges import Coinbase

basecoin_fp = './basecoindata.db'
basecoins = ['BTC','LTC','ETH']
quotecoin = 'USD'
max_latency = 5 
strtime = "%Y-%m-%d-%M-%S"
markets = [bc + "/" + quotecoin for bc in basecoins]
market_names = [bc + "_" + quotecoin for bc in basecoins]

#create an object for each exchange as we add them; custom funcs to handle each inner data discrepancies
#then we call a registrar that inits and holds all of the exchange objects
#we should be able to call the registrar & a coin, it should return all the available markets for the coin


class Basecoin_monitor(object):
    """
    Allows us to actively monitor basecoins in terms of the quotecoin
    """

    def __init__(self):
        #connect to database or create if none exists
        if not os.path.isfile(basecoin_fp):
            bc_conn = sqlite3.connect(basecoin_fp)
            bc_c = bc_conn.cursor()
            for name in market_names:
                bc_c.execute("CREATE TABLE IF NOT EXISTS " + name + "(datestamp DATETIME, ask REAL, bid REAL)")
                bc_conn.commit()
        else:
            bc_conn = sqlite3.connect(basecoin_fp)
            bc_c = bc_conn.cursor()

        self.conn = bc_conn
        self.cur = bc_c

        #begin connection with coinbase
        cb = Coinbase()
        self.cb = cb

    def close_db(self):
        self.cur.close()
        self.conn.close()

    def push_askbid(self, timestamp, askbid_dict):
        for name in market_names: 
            (lowest_ask, highest_bid) = (askbid_dict[name]['ask'], askbid_dict[name]['bid'])
            self.cur.execute("INSERT INTO " + name + " values (?, ?, ?)", (timestamp, lowest_ask, highest_bid))
            self.conn.commit()

    def begin_stream(self, verbose=False):
        try:
            while(True):
                ts, askbid = self.cb.grab_basecoins_askbid()
                if verbose:
                    print(askbid)
                self.push_askbid(ts, askbid)
                time.sleep(5)
        finally:
            self.close_db()


### MAIN

bc = Basecoin_monitor()
bc.begin_stream(True)

