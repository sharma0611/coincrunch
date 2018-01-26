
import ccxt
import pandas
import sqlite3
import os.path
from datetime import datetime 
import time
import pymysql

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

#whether to save streaming data locally or to RDS
local = False

#create an object for each exchange as we add them; custom funcs to handle each inner data discrepancies
#then we call a registrar that inits and holds all of the exchange objects
#we should be able to call the registrar & a coin, it should return all the available markets for the coin

class Database(object):

    def __init__(self, local_bool):
        if local_bool:
            bc_conn = sqlite3.connect(basecoin_fp)
            bc_c = bc_conn.cursor()
        else:
            import config
            bc_conn = pymysql.connect(config.host, user=config.user, port=config.port, passwd=config.password,
                    db=config.dbname)
            bc_c = bc_conn.cursor()


        self.conn = bc_conn
        self.cur = bc_c

    def close_db(self):
        self.cur.close()
        self.conn.close()

    def get_cursor():
        return self.cur

    def get_connection():
        return self.conn

class Basecoin_monitor(object):
    """
    Allows us to actively monitor basecoins in terms of the quotecoin
    """

    def __init__(self):
        db = Database(local)
        self.db = db


        self.conn = db.get_connection()
        self.cur = db.get_cursor()

        #begin connection with coinbase
        cb = Coinbase()
        self.cb = cb

        #create tables if not there
        for name in market_names:
            self.cur.execute("CREATE TABLE IF NOT EXISTS " + name + "(datestamp DATETIME, ask REAL, bid REAL)")
            self.conn.commit()

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
                time.sleep(3)
        finally:
            self.db.close_db()

### MAIN

bc = Basecoin_monitor()
bc.begin_stream(True)

