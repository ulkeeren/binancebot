from binance.um_futures import UMFutures
import plotly.graph_objects as go
import requests
import json
import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import datetime
from chart import Chart

api_key ="iPQMe46exUy10KiBaBahQT7ow1uzb9jaxlKj19Bg5BI8JEwJL5bw9LCvJtfKuVbP"
secret_key = "J4FGJQdGPpNGm8jpnj3IuFuDJuAe7FIa3cM51L4z662UYux3qD0ByLJ0bfIltZvK"

def convert_to_df(data):
        data_df=pd.DataFrame(np.asarray(data,dtype=np.float64),columns=["Open Time","Open","High","Low","Close","Volume","Close Time","Quote Asset Volume","Number of Trades","Taker Buy Volume","Taker Buy Quote Asset Volume","Ignore"])
        data_df['Open Time'] = pd.to_datetime(data_df['Open Time'], unit='ms')
        data_df['Close Time'] = pd.to_datetime(data_df["Close Time"],unit='ms').dt.ceil("min")
        return data_df.drop("Ignore",axis=1)

um_futures_client = UMFutures()
um_futures_client = UMFutures("iPQMe46exUy10KiBaBahQT7ow1uzb9jaxlKj19Bg5BI8JEwJL5bw9LCvJtfKuVbP","J4FGJQdGPpNGm8jpnj3IuFuDJuAe7FIa3cM51L4z662UYux3qD0ByLJ0bfIltZvK")
bake_data = convert_to_df(um_futures_client.continuous_klines("BAKEUSDT","PERPETUAL","15m"))
bake_chart = Chart(bake_data)
bake_chart.plot()

