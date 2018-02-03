# coincrunch
Let's crunch some cryptos.

### This repo is currently under development.

Coincrunch is going to be the easiest way to pipeline crypto data straight from exchange API's to local/cloud infrastructure. 

After the data is yours, you can use it for data science or interactive visualization.

You can also add your own API keys to perform your own transactions.

Use our interactive visualizations to pull up live bids, asks, market tickers on over 20 exchanges.

Current API's & python libraries for cryptos are very thorough; the goal is to make something that works for simple command line needs.

## What you need

* **Python 3**
* Use virtualenv, but it's not crucial.

## Quick Setup

Current features are extremely limited.

1) **Install**

```bash
$ git clone https://github.com/sharma0611/coincrunch.git
$ cd coincrunch
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements
```

2) **Configure**

Connect our analytics pipeline to an Amazon RDS instance running PostgreSQL.

All you need to do is add your credentials to coincrunch/config.cfg

Use our template in coincrunch/config.cfg.template

3) **Pump Data**

Now you can run the following:

```bash
$ python coincrunch.py
```

This will stream live bid/ask data to your instance as long as you keep it running.
Tables are formatted as such:
table name: <exchange id> 
table columns: <datestamp, bid, ask, market, market_sym> 

Where <exchange_id> and <market> are source directly from your config.cfg file. These must be valid values with one of our supported exchanges & markets. 

For now, use the values in our template config.cfg.

4) **Visualize your data**

Run the following to visualize your data on a live streaming bokeh dashboard. See latest prices as they come in, all from your web browser!

```bash
$ python dashboard.py
```

Under the hood, you can see Exchange & databasing classes made to keep track of data, parse different signatures of the same coins, and ultimately produce an interactive dashboard for trading & viewing historical data.

5) **Next Steps**

This repo is under heavy development and features can change at any moment. Currently, adding more features for the dashboard & support for more exchanges and more markets. 
