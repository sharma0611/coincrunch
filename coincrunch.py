#!/usr/bin/env python3

import pandas
import os.path
from datetime import datetime 
import time

import matplotlib.pyplot as plt
import numpy as np
from common.exchanges import Coinbase

max_latency = 5 
strtime = "%Y-%m-%d %H:%M:%S"

#create an object for each exchange as we add them; custom funcs to handle each inner data discrepancies
#then we call a registrar that inits and holds all of the exchange objects
#we should be able to call the registrar & a coin, it should return all the available markets for the coin


basecoin_db_name = "basecoindata"
local = False
basecoins = ['BTC','LTC','ETH']
quotecoin = 'USD'


### MAIN
bc = Basecoin_monitor()
bc.begin_stream(True)

