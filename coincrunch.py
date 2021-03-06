#!/usr/bin/env python3

from lib.monitor import Monitor
from lib.config import Config
from lib.logger import start_printer, end_printer
import ast
import time
from datetime import datetime
import traceback

strtime = "%Y-%m-%d %H:%M:%S"
local = False

### MAIN
metadata = Config.get_variable("monitor", "metadata")
metadata = ast.literal_eval(metadata)
mc = Monitor(metadata)

start_printer("logs", datetime.now().strftime(strtime).replace(" ", "") + "_main.log")

while True:
    try:
        now = datetime.now()
        num_markets = mc.update_data()
        end = datetime.now()
        print("Updated " + str(num_markets) + " markets in " + str((end-now).total_seconds()) + " s." )
    except Exception as e: 
        print("Encountered Exception: " + str(e))
        print(traceback.format_exc())
        break

end_printer()
