import data_ops
import pandas as pd
import numpy as np
import vectorbt as vbt
dg = data_ops.DataGetter()
def donchian_strat(data_in,window = 14):
    #DCL_14_14  DCM_14_14  DCU_14_14
    donchian_df = dg.donchian(data_in,window)
    rdf= pd.DataFrame()
    rdf["long_entries"] = data_in[(data_in["Close"] <= donchian_df["DCU_14_14"]) & (donchian_df["DCU_14_14"] <= data_in["High"])]["Open Time"] #Long entry
    rdf["exit"] = data_in[(data_in["Close"] <= donchian_df["DCM_14_14"]) & (donchian_df["DCM_14_14"] <= data_in["Open"]) | (data_in["Open"] <= donchian_df["DCM_14_14"]) & (donchian_df["DCM_14_14"] <= data_in["Close"]) ]["Open Time"]
    rdf["short_entries"] = data_in[(data_in["Low"] <= donchian_df["DCL_14_14"]) & (donchian_df["DCL_14_14"] <= data_in["Close"])]["Open Time"] #Short entry
    
    price = data_in["Close"]
    signals = pd.DataFrame()
    signals["Open Time"] = data_in["Open Time"]
    signals["Long Signal"] = signals["Open Time"].isin(rdf["long_entries"])
    signals["Short Signal"] = signals["Open Time"].isin(rdf["short_entries"])
    signals["Exit Signal"] = signals["Open Time"].isin(rdf["exit"])
    signals = signals.set_index("Open Time")
    signals.index.name = ""
    return signals
    

