import io
import requests
import pandas as pd
from bokeh.models import ColumnDataSource, HoverTool, SaveTool, DatetimeTickFormatter
from bokeh.models.widgets import TextInput, Button
from bokeh.plotting import figure, curdoc
from bokeh.layouts import row, widgetbox, column
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
initial_window = 1200 #specify # of mins of data to initially grab

#each market will take one plot
#each data attribute will take one line; must match column name of data in db
data_attributes = ["ask", "bid"]

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
curr_markets = df['market'].unique().tolist()
pivot_df = df.pivot(index='datestamp', columns='market')

#to hold {market_name: data_object}
market_data_dict = {}
market_plots = []

#make a graph for each market
for market in curr_markets:
    #create a figure for the market
    hover = HoverTool(tooltips=[("Time", "@x{%F}")])
    market_plot = figure(plot_width=800,
                        plot_height=400,
                        x_axis_type='datetime',
                        tools=[hover, SaveTool()],
                        title= exch.upper() + " Data: " + market )
    market_plot.xaxis.axis_label = "Time"
    market_plot.yaxis.axis_label = "Price"
    market_plot.title.text = "Real Time Data for " + market

    mypalette=Spectral11[0:len(data_attributes)]

    for idx, data_attr in enumerate(data_attributes):
        #create a plot for each data attribute
        curr_df = pivot_df[data_attr][[market]]
        curr_df.dropna(inplace=True)
        x = curr_df.index.values
        y = curr_df[market].values
        curr_data = ColumnDataSource(dict(x=x,y=y))
        market_data_dict[(market, data_attr)] = curr_data
        market_plot.line(x='x',y='y', source=curr_data, color=mypalette[idx], legend=data_attr.capitalize())

    market_plots.append(market_plot)


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

curdoc().add_root(column(*market_plots, width=1600))
curdoc().title = "Real-Time Price Plot from IEX"
#curdoc().add_periodic_callback(update_price, 1000)
