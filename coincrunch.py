#!/usr/bin/env python3

from lib.monitor import Monitor
from lib.config import Config

max_latency = 5 
strtime = "%Y-%m-%d %H:%M:%S"
basecoin_db_name = "basecoindata"
local = False
basecoins = ['BTC','LTC','ETH']
quotecoin = 'USD'

### MAIN
metadata = Config.get_variable("monitor", "metadata")
mc = Monitor(metadata)

while True:
    mc.update_data()
    time.sleep(5)
