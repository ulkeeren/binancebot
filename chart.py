import plotly.graph_objects as go
import pandas as pd
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
        
    def plot(self):
        self.figure.show()

    def add_line(self,line_name,*args):
        #args 0 ve 1 dtype: 
        line = go.Scatter(x=[args[0], args[1]], y=[args[2], args[3]], mode='lines', line=dict(color='green'), name=line_name)
        self.figure.add_trace(line)

    def delete_line(self,line_name):
        self.figure.data = [trace for trace in self.figure.data if trace.name != line_name]
    
    #TODO: Gradient Descent fonksiyonu

    #Fonksiyonu swing high ve swing lowlara göre yapmaya çalışayım ki daha net trendlinelar belirlesin

    #Swing H-L yapmadan da lineın kesiştiği yere kadar devam ettirip ona göre lineın slopeunu yavaş yavaş azaltarak optimize edebilirim
    def gradient_descent(self, data):
        #0 slope 1 intercept
        X = data["Low"].index.values.reshape(-1,1)
        y = data["Low"]
        linear_regression = LinearRegression()
        linear_regression.fit(X,y)
        return [linear_regression.coef_[0], linear_regression.intercept_]
    
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
    #def auto_draw_line(self,begin,end):
        