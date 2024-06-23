from binance.um_futures import UMFutures
import requests
import pandas as pd
import os
import math
from pandas_ta.volatility import atr
from pandas_ta.volatility import donchian
from pandas_ta.volatility import bbands
from pandas_ta.overlap import supertrend
import numpy as np
from pandas import Timestamp
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import time

class DataGetter:
    def __init__(self,api_key=0,api_secret=0 ):
        self.base_endpoint = "https://fapi.binance.com"
        self.api_key = api_key
        self.api_secret = api_secret
        if api_key != 0 and api_secret != 0:
            self.client = UMFutures("iPQMe46exUy10KiBaBahQT7ow1uzb9jaxlKj19Bg5BI8JEwJL5bw9LCvJtfKuVbP","J4FGJQdGPpNGm8jpnj3IuFuDJuAe7FIa3cM51L4z662UYux3qD0ByLJ0bfIltZvK")
    

    def fetch_whitelist_data(self):
        intervals = ["1m","5m","15m","1h","4h"]
        whitelist = open(r"D:\binanceapi\whitelist.txt")
        for l in whitelist:
            for interval in intervals:
                self.get_all_pair_data_past(pair_in=l[:-1],interval_in=interval)


    def replace_market_file(self,pair_in,interval_in):
        os.remove(f"D:\\binanceapi\\MarketData\\{pair_in}\\{pair_in}_{interval_in}.csv")
        os.rename(f"D:\\binanceapi\\{pair_in}_{interval_in}.csv", f"D:\\binanceapi\\MarketData\\{pair_in}\\{pair_in}_{interval_in}.csv")
    
    
    def get_all_pair_data_past(self,**kwargs):
        if not os.path.exists(f"D:\\binanceapi\\MarketData\\{kwargs["pair_in"]}\\{kwargs["pair_in"]}_{kwargs["interval_in"]}.csv"):
            print(f"D:\\binanceapi\\MarketData\\{kwargs["pair_in"]}_{kwargs["interval_in"]}.csv")
            df=pd.DataFrame()
            try:
                df = self.get_pair_data(**kwargs)
            except:
                print(f"Can't fetch {kwargs["pair_in"]}")
                return
            while True:
                try:
                    unix=self.datetime_to_unix(df["Open Time"])
                    df_before = self.get_pair_data("BTCUSDT",interval_in=kwargs["interval_in"],endTime=unix[0])
                    df=pd.concat([df_before,df],axis = 0)
                except:
                    break

            df.to_csv(f"{kwargs["pair_in"]}_{kwargs["interval_in"]}.csv",index = False)
            try:
                os.rename(f"D:\\binanceapi\\{kwargs["pair_in"]}_{kwargs["interval_in"]}.csv", f"D:\\binanceapi\\MarketData\\{kwargs["pair_in"]}\\{kwargs["pair_in"]}_{kwargs["interval_in"]}.csv")
            except FileNotFoundError:
                os.makedirs(f"D:\\binanceapi\\MarketData\\{kwargs["pair_in"]}")
                os.rename(f"D:\\binanceapi\\{kwargs["pair_in"]}_{kwargs["interval_in"]}.csv", f"D:\\binanceapi\\MarketData\\{kwargs["pair_in"]}\\{kwargs["pair_in"]}_{kwargs["interval_in"]}.csv")
            return df

    def get_pair_data(self,pair_in,interval_in,**kwargs):
        return self.convert_to_df(self.client.continuous_klines(pair_in,contractType="PERPETUAL", interval=interval_in,limit=1000,**kwargs))
    
    def get_pair_data_past(self,pair_in,interval_in="1m",lenght=1000):
        toy_data = data_getter.get_pair_data(pair_in,interval_in)
        end_date = toy_data.iloc[0]["Open Time"]
        for i in range(lenght):
            toy_data = pd.concat([data_getter.get_pair_data(pair_in,interval_in,endTime=data_getter.datetime_to_unix(toy_data.iloc[0]["Open Time"])),toy_data])
        return toy_data
       
    def convert_to_df(self, data):
        data_df=pd.DataFrame(np.asarray(data,dtype=np.float64),columns=["Open Time","Open","High","Low","Close","Volume","Close Time","Quote Asset Volume","Number of Trades","Taker Buy Volume","Taker Buy Quote Asset Volume","Ignore"])
        data_df['Open Time'] = pd.to_datetime(data_df['Open Time'], unit='ms')
        data_df['Close Time'] = pd.to_datetime(data_df["Close Time"],unit='ms').dt.ceil("min")
        data_df["Index"] = np.arange(len(data))
        return data_df.drop("Ignore",axis=1)
    
    def backtesting_preprocessing(self,data_in):
        returnDF = data_in[["Open","High","Low","Close","Volume","Open Time"]].set_index("Open Time")
        returnDF.index.name=""
        #returnDF["Open Time"] = returnDF.index.values
        return returnDF
        
    def datetime_to_unix(self,dates):
        return (dates - pd.Timestamp("1970-01-01")) // pd.Timedelta('1ms')
        
    def get_valid_pairs(self):
        exchange_info_endpoint = self.base_endpoint + "/fapi/v1/exchangeInfo"
        response = requests.get(exchange_info_endpoint)
        if response.status_code == 200:
            exchange_info = response.json()
            return [symbol["symbol"] for symbol in exchange_info['symbols']]
    
    """
    def get_pair_data(self,pair,interval,limit=500):
        
        return requests.get("https://fapi.binance.com/fapi/v1/klines?symbol={pair}&interval={interval}&limit={limit}")  bu 1. secenek
        r = requests.get("https://fapi.binance.com/fapi/v1/klines?symbol=BAKEUSDT&interval=1m&limit=500")
        print(r.json())
        bu çalışıyor

    def data(self,pair,interval,limit=500):
        return self.convert_to_df(requests.get("https://fapi.binance.com/fapi/v1/klines?symbol={pair}&interval={interval}&limit={limit}").json())
    """
    




    """
    Indicator returning functions
    """
    def ema(self,data_in,mode_in="Low", order = 15):
        line_values = []
        dates = []
        c=1
        for idx in range(order,len(data_in)):
            t=0       
            for value in data_in.iloc[ idx-order : idx ][mode_in]:
               t += value
            line_values.append(t / order)
            dates.append(data_in.iloc[idx]["Open Time"])
        return dates,line_values
    
    def atr(self,data_in,window=14):
        return atr(data_in["High"],data_in["Low"],data_in["Close"],lenght = window )
    
    def Bollinger(self,data_in,window=14):
        return bbands(data_in["Close"],length=window)
    
    def donchian(self,data_in,window=14):
        return donchian(data_in["High"],data_in["Low"],upper_length=window, lower_length=window)
    
    def superTrend(self,data_in,window=14):
        return supertrend(data_in["High"],data_in["Low"],data_in["Close"],window)
        