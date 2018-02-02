import io
import requests
import pandas as pd
from bokeh.models import ColumnDataSource, HoverTool, SaveTool, DatetimeTickFormatter
from bokeh.models.widgets import TextInput, Button
from bokeh.plotting import figure, curdoc
from bokeh.layouts import row, widgetbox
from bokeh.palettes import Spectral11

from lib.db import DB
from lib.config import Config
import ast
import datetime

#must be same as markets specified in metadata
strtime = "%Y-%m-%d %H:%M:%S"
display_exchanges = ["gdax"]
#display_exchanges = []
display_markets = []
initial_window = 100000 #specify # of mins of data to initially grab

#grab dataframe we need
#ensure exchanges are available
metadata = Config.get_variable("monitor", "metadata")
metadata = ast.literal_eval(metadata)
supported_markets = list(metadata.keys())
assert all([i in display_exchanges for i in supported_markets])

#for each exchange
exch = display_exchanges[0] #need to invent for loop here after this works

now = datetime.datetime.now()
before = now - datetime.timedelta(minutes=initial_window)

query = "SELECT * FROM " + exch + " WHERE datestamp BETWEEN '" + before.strftime(strtime) + "' AND '" + now.strftime(strtime) + "'" 
db = DB()
df = db.execute_and_grab_df(query)
df.drop('market_sym', axis=1, inplace=True)
pivot_df = df.pivot(index='datestamp', columns='market')
ask_df = pivot_df['ask']
bid_df = pivot_df['bid']

#to hold {market_name: data_object}
market_data_dict = {}

#make a graph for each market
for market in ask_df.columns.tolist():
    market_ask_df = ask_df[[market]]
    market_bid_df = bid_df[[market]]
    market_ask_df.dropna(inplace=True)
    market_bid_df.dropna(inplace=True)
    xs = [market_ask_df.index.values, market_bid_df.index.values]
    ys = [market_ask_df[market].values, market_bid_df[market].values]
    market_data = ColumnDataSource(dict(xs=xs, ys=ys))
    market_data_dict[market] = market_data
    mypalette=Spectral11[0:2]

    hover = HoverTool(tooltips=[
        ("Time", "@datestamp")
       # ("Ask", "@ask")
       # ("Bid", "@bid")
        ])

    price_plot = figure(plot_width=800,
                        plot_height=400,
                        x_axis_type='datetime',
                        tools=[hover, SaveTool()],
                        title="Ask/Bid Plot: " + market )

    price_plot.multi_line(xs='xs', ys='ys', source=market_data, line_width=5)
    price_plot.xaxis.axis_label = "Time"
    price_plot.yaxis.axis_label = "Cryptos Real-Time Price"
    price_plot.title.text = "Cryptos Real Time Price"

    break

#base = "https://api.iextrading.com/1.0/"
#
#def get_last_price(symbol):
#    payload = {
#        "format": "csv",
#        "symbols": symbol
#    }
#    endpoint = "tops/last"
#
#    raw = requests.get(base + endpoint, params=payload)
#    raw = io.BytesIO(raw.content)
#    prices_df = pd.read_csv(raw, sep=",")
#    prices_df["time"] = pd.to_datetime(prices_df["time"], unit="ms")
#    prices_df["display_time"] = prices_df["time"].dt.strftime("%m-%d-%Y %H:%M:%S.%f")
#
#    return prices_df
#
#def update_ticker():
#    global TICKER
#    TICKER = ticker_textbox.value
#    price_plot.title.text = "IEX Real-Time Price: " + ticker_textbox.value
#    data.data = dict(time=[], display_time=[], price=[])
#
#    return
#
#def update_price():
#    new_price = get_last_price(symbol=TICKER)
#    data.stream(dict(time=new_price["time"],
#                     display_time=new_price["display_time"],
#                     price=new_price["price"]), 10000)
#    return


#hover = HoverTool(tooltips=[
#    ("Time", "@datestamp"),
#    ("IEX Real-Time Price", "@price")
#    ])
#
#price_plot = figure(plot_width=800,
#                    plot_height=400,
#                    x_axis_type='datetime',
#                    tools=[hover, SaveTool()],
#                    title="Real-Time Price Plot")
#
#price_plot.line(source=data, x='time', y='price')
#price_plot.xaxis.axis_label = "Time"
#price_plot.yaxis.axis_label = "IEX Real-Time Price"
#price_plot.title.text = "IEX Real Time Price: " + TICKER
#
#ticker_textbox = TextInput(placeholder="Ticker")
#update = Button(label="Update")
#update.on_click(update_ticker)

#inputs = widgetbox([ticker_textbox, update], width=200)

curdoc().add_root(row(price_plot, width=1600))
curdoc().title = "Real-Time Price Plot from IEX"
#curdoc().add_periodic_callback(update_price, 1000)
