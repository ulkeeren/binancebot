from binance.um_futures import UMFutures
import requests
import pandas as pd
import numpy as np
class DataGetter:
    #TODO: data getter classının hangi variablelara ihtiyacı olduğunu tespit etmem lazım
    def __init__(self,api_key,api_secret ):
        self.base_endpoint = "https://fapi.binance.com"
        self.api_key = api_key
        self.api_secret = api_secret
    
    def convert_to_df(self,data):
        data_df=pd.DataFrame(np.asarray(data,dtype=np.float64),columns=["Open Time","Open","High","Low","Close","Volume","Close Time","Quote Asset Volume","Number of Trades","Taker Buy Volume","Taker Buy Quote Asset Volume","Ignore"])
        data_df['Open Time'] = pd.to_datetime(data_df['Open Time'], unit='ms')
        data_df['Close Time'] = pd.to_datetime(data_df["Close Time"],unit='ms').dt.ceil("min")
        return data_df
        
    #TODO: Kullanılmıyor şu anda, kullanilabilir hale sonra getiririm
    def get_valid_pairs(self):
        exchange_info_endpoint = self.base_endpoint + "/fapi/v1/exchangeInfo"
        response = requests.get(exchange_info_endpoint)
        if response.status_code == 200:
            exchange_info = response.json()
            return [symbol for symbol in exchange_info['symbols']]
    
    #TODO: 
    def get_pair_data(self,pair,interval,limit=500):
        #TODO: nasıl getlemem gerektiğini bulmam lazım
        #return requests.get("https://fapi.binance.com/fapi/v1/klines?symbol={pair}&interval={interval}&limit={limit}")  bu 1. secenek
        """
        r = requests.get("https://fapi.binance.com/fapi/v1/klines?symbol=BAKEUSDT&interval=1m&limit=500")
        print(r.json())
        bu çalışıyor
        """

    def data(self,pair,interval,limit=500):
        return self.convert_to_df(requests.get("https://fapi.binance.com/fapi/v1/klines?symbol={pair}&interval={interval}&limit={limit}").json())


    

    