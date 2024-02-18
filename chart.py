import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pandas import Timestamp
from sklearn.linear_model import LinearRegression


class Chart:
    #TODO: candlestick verisi input alacak fonksiyonlar için standart bir input proseduru yaz 
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
        # args 0, 1 dtype: int, index
        # args 2, 3 dtype: np.float64 price of a candlestick 
        line_color = dict(color='green')
        if mode == "High":
            line_color = dict(color='red') 
        line = go.Scatter(x=[args[0], args[1]], y=[args[2], args[3]], mode='lines', line=dict(color='green'), name=line_name)
        self.line_name_list.append(line_name)
        self.figure.add_trace(line)

    def delete_line(self,line_name):
        self.figure.data = [trace for trace in self.figure.data if trace.name != line_name]
    
    #TODO: Gradient Descent fonksiyonu

    #Fonksiyonu swing high ve swing lowlara göre yapmaya çalışayım ki daha net trendlinelar belirlesin

    #Swing H-L yapmadan da lineın kesiştiği yere kadar devam ettirip ona göre lineın slopeunu yavaş yavaş azaltarak optimize edebilirim

    #TODO: line opt eğer elimdeki bütün datada çizilen bir line varsa doğru çalışıyor çünkü 
    def line_opt(self,line,data_in,mode="Low"):
        """
        line: list containing slope [0] and intercept [1] of a  line
        """
        dif_list = data_in[mode] - (line[0]*data_in[mode]+line[1])
        min_dif_idx = dif_list.argmin()
        min_dif = dif_list.iloc[min_dif_idx]
        return [(min_dif/min_dif_idx) - line[0] , line[1]] 
        
    
    def gradient_descent(self, data_in,mode_in="Low"):
        """
        data_in = pd dataframe
                  ["Low"] ya da başka bir şey kullanma, mode input alan bütün fonksiyonlara dataframe girdisi yap
        """
        
        X = (data_in["Open Time"].astype(np.int64) // (9 * 10**11)) # Eğer (9 * 10 ** 11) bunla bölersek 1970 tarihi returnlüyo , - (data_in["Open Time"].iloc[0] // (9 * 10**11)
                                                                    #                                                               yaparsak da indexleri float olarak veriyor
                                                                    # pd.to_datetime kullanabilmek için (9 * 10 ** 11) ile çarpmak lazım

        y = data_in[mode_in]
        line_a = (data.iloc[-1]["Low"] - data.iloc[0]["Low"]) / ((data.iloc[499]["Close Time"] - data.iloc[200]["Open Time"]).value) * 9 * 10**11
        line_b = data.iloc[200]["Low"]
        #return self.line_opt([linear_regression.coef_[0], linear_regression.intercept_],data_in = data_in,mode=mode_in)
        
        
    
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
            idx = self.data[self.data["Open Time"] == arg["Open Time"]].index

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


        

    #TODO: Swing High ve Swing Low bulma
    #Swingleri etraftaki kaç muma göre arayacağıma karar vermem lazım, onu da range parametresiyle ayarlarım,
    #ilerde belki modele feedleyeceğim zaman bikaç rangede buldurur ve pcaini aldırırım
    def find_swings(self,range):
        for index,row in self.data.iterrows():
            print(candlestick)

        
    #TODO: Support ve Resistance Çizme
    

    #TODO: Trend Çizme
    def auto_draw_line(self,data_in, begin = 0,end = 499, mode = "Low"):
        #TODO: trend başlagngıç ve bitiş mumları bulma fonksiyonu, onları yazana kadar begin ve end parametreleri kalacak

        if max(data_in.index.values.reshape(-1,1)) < 499:
            end = data_in.iloc[-1].index.values.reshape(-1,1) 
        data_to_be_processed = data_in.iloc[begin:end+1]
        line = self.gradient_descent(data_in=data_to_be_processed,mode_in = mode)
        self.add_line("test_auto_draw", data_in.iloc[begin]["Open Time"], data_in.iloc[end]["Close Time"],data_in.iloc[begin][mode],data_in.iloc[end][mode])
        #self.data[self.data["Open Time"] == data_in.iloc[end]["Low"]].index