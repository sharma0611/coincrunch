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

```bash
$ git clone https://github.com/sharma0611/coincrunch.git
$ cd coincrunch
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements
$ python coincrunch.py
```

This begins a livestream of highest bid & lowest ask prices on GDAX, the coinbase exchange.

Under the hood, you can see Exchange & databasing classes made to keep track of data, parse different signatures of the same coins, and ultimately produce an interactive dashboard for trading & viewing historical data.
