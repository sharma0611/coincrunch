#!/usr/bin/env python3

from lib.monitor import Monitor
from lib.config import Config
import ast
import time
from datetime import datetime

max_latency = 5 
strtime = "%Y-%m-%d %H:%M:%S"
basecoin_db_name = "basecoindata"
local = False
basecoins = ['BTC','LTC','ETH']
quotecoin = 'USD'

### MAIN
metadata = Config.get_variable("monitor", "metadata")
metadata = ast.literal_eval(metadata)
mc = Monitor(metadata)

while True:
    now = datetime.now()
    mc.update_data()
    end = datetime.now()
    sleep_time = max(0, 5 - (end - now).total_seconds())
    print(sleep_time)
    time.sleep(sleep_time)
