from lib.DB import DB
import lib.exchanges as exch 

#metadata:
# {exchange_name: [(base_coin, quote_coin), (base_coin, quote_coin), ... ]
#  exchange_name1 : ... 
#  ... }

class Monitor(object):
    """
    Allows us to actively monitor certain coins on exchanges & updates values to database
    """

    def __init__(self, metadata):
        self.db = DB()
        self.metadata = metadata

        #begin connection with coinbase
        cb = exch.Coinbase()
        self.cb = cb

        #create market symbols & names to be recorded for basecoins
        market_names = create_market_names(Basecoin_monitor.quotecoin, Basecoin_monitor.basecoins)

        #create tables if not there
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

