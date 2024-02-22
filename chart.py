import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pandas import Timestamp
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler



class Chart:
    def __init__(self,data):
        self.data = data
        self.candlesticks = go.Candlestick(x=self.data['Open Time'],
                open=self.data['Open'],
                high=self.data['High'],
                low=self.data['Low'],  
                close=self.data['Close'],name="Candlesticks")
        self.figure = go.Figure(self.candlesticks)
        self.line_name_list = []        
        
    def plot(self):
        self.figure.show()

    def add_line(self,line_name,*args,mode="Low"):
        line_color = dict(color='green')
        if mode == "High":
            line_color = dict(color='red') 
        line = go.Scatter(x=[args[0], args[1]], y=[args[2], args[3]], mode='lines', line=dict(color='green'), name=line_name)
        self.line_name_list.append(line_name)
        self.figure.add_trace(line)
        self.figure.update_layout(showlegend=True)

    def add_line_2_candles(self, candle_1,candle_2,mode="Low",line_name="porno"):
        line_color = dict(color='green')
        if mode == "High":
            line_color = dict(color='red') 
        line = go.Scatter(x=[candle_1["Open Time"], candle_2["Close Time"]], y=[candle_1["Low"], candle_2["Low"]], mode='lines', line=dict(color='green'), name=line_name)
        self.line_name_list.append(line_name)
        self.figure.add_trace(line)

    def draw_line_between_dates(self, candle_1,candle_2,mode = "Low"):
        self.add_line("t1",candle_1["Open Time"],candle_2["Open Time"],candle_1[mode], candle_2[mode])
        
    def add_vertical_line(self,candle_1,candle_2,value,line_name = "vertical line"):
        self.add_line(line_name, candle_1["Open Time"],candle_2["Open Time"],value,value)
        self.line_name_list.append(line_name)


    def delete_line(self,line_name):
        self.figure.data = [trace for trace in self.figure.data if trace.name != line_name]
    
    
    
    def line_opt(self,line,data_in,mode="Low"):
        #line: list containing slope [0] and intercept [1] of a  line
        dif_list = data_in[mode] - (line[0]*data_in[mode]+line[1])
        min_dif_idx = dif_list.argmin()
        min_dif = dif_list.iloc[min_dif_idx]
        return [(min_dif/min_dif_idx) - line[0] , line[1]] 
    
    
    def init_line(self, data_in,mode_in="Low"):
        #TODO: gives a decent line but needs optimization
        reg = LinearRegression()
        #X=np.arange(len(data_in)).reshape(-1, 1)
        X=data_in["Index"].values.reshape(-1, 1)
        y=data_in[mode_in].values.reshape(-1,1)
        reg.fit(X,y)
        return reg.coef_[0][0],reg.intercept_[0]
        
    
    

    
    #TODO: Herhangi bir candlestickin open-close arasından geçiyor bir line onun kontrolünü yapan fonksiyon
    def check_oc_collision_of_single_candlestick(self,arg,line,mode="Open Time"):
        """
        input
            arg: bir pandas dataframeinin rowu da olabilir (pandas.core.series.Series),    
                  index de olabilir (int),
                  tarih de olabilir (pandas._libs.tslibs.timestamps.Timestamp)
                bunu şimdilik bir trendline çizdiğimizde trendline başlangiç mumundan itibaren ilerdeki diğer mumlarla çakişip çakişmadiğini bir for loop içinde
                bulmak için kullanicaz,
                TODO: ileride bunu trendline başlangic mumunu tespit edebildiğimde trendline mumunu doğrulamak için kullanicaz

            line:
                regresyon sonucu elde ettiğimiz slope ve intercept, slope'u indexle çarpinca regresyon linei çikiyor.
                yani diğer data tiplerini timestampe çevirmek lazim
            mode:
                Open Time ya da Close Time'a göre algoritmayi çaliştirmak için aldiğimiz bir parametre
        """
        idx = 0
        #dataframe row case
        if type(arg) == "pandas.core.series.Series":
            idx = self.data[self.data["Open Time"] == arg["Open Time"]]["Index"]

        #int case
        elif type(arg) == "int":
            idx=arg

        #timestamp case
        elif type(arg)=="pandas._libs.tslibs.timestamps.Timestamp":
            idx = self.data[self.data["Open Time"] == arg].index
        
        return (    [self.data.iloc[idx]["Open Time"] ,self.data.iloc[idx]["Close"] <= line[0]*idx+line[1] <= self.data.iloc[idx]["Open"] 
                    or
                    self.data.iloc[idx]["Open"] <= line[0]*idx+line[1] <= self.data.iloc[idx]["Close"]]    
                )
    
    def check_oc_collisions(self,begin,end,line):
        collision_list = [] #bu liste [bool,timestamp] veri türünde olacak şekilde candlesticklerin istenen linela çakışıp çakışmadığını tutacak 
        begin_idx = begin
        while begin_idx != end+1:
            collision_list.append(self.check_oc_collision_of_single_candlestick(begin_idx,line))
            begin_idx += 1

        return collision_list

    def low_swings(self,data_in,order=2):
        low_swing_list = []
        for i in range(order,len(data_in)-order):
            flag = True
            for j in range(1,order+1):
                if data_in.iloc[i]["Low"] > data_in.iloc[i+j]["Low"] or data_in.iloc[i]["Low"] > data_in.iloc[i-j]["Low"]:
                    flag=False
                    break
            if flag == True:
                low_swing_list.append(data_in.iloc[i]["Index"])
            
        return low_swing_list
    
    def high_swings(self,data_in,order=2):
        high_swing_list = []
        for i in range(order,len(data_in)-order):
            flag = True
            for j in range(1,order+1):
                if data_in.iloc[i]["High"] < data_in.iloc[i+j]["High"] or data_in.iloc[i]["High"] < data_in.iloc[i-j]["High"]:
                    flag=False
                    break
            if flag == True:
                high_swing_list.append(data_in.iloc[i]["Index"])
            
        return high_swing_list
    #TODO: line grafikte gözükmüyor, onu çöz
    
    def draw_support(self,data_in,order=15):
        sup_list=[]
        smallest_15 = data_in.nsmallest(order,"Low")
        average_order = np.sum(smallest_15["Low"].values.reshape(-1,1)) / order
        self.add_vertical_line(smallest_15.nsmallest(1,"Index").iloc[0],smallest_15.nlargest(1,"Index").iloc[0],average_order)



            