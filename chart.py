import plotly.graph_objects as go
class Chart:
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
        line = go.Scatter(x=[args[0], args[1]], y=[args[2], args[3]], mode='lines', line=dict(color='green'), name=line_name)
        self.figure.add_trace(line)

    def delete_line(self,line_name):
        self.figure.data = [trace for trace in self.figure.data if trace.name != line_name]
    
    #TODO: Gradient Descent fonksiyonu
    #Fonksiyonu swing high ve swing lowlara göre yapmaya çalışayım ki daha net trendlinelar belirlesin
    #Swing H-L yapmadan da lineın kesiştiği yere kadar devam ettirip ona göre lineın slopeunu yavaş yavaş azaltarak optimize edebilirim
    def gradient_descent(self):
        #0 slope 1 intercept
        linear_regression = LinearRegression()
        linear_regression.fit(self.data["Low"].index.values.reshape(-1,1),self.data["Low"])
        return [linear_regression.coef_[0], linear_regression.intercept_]
        
        

    #TODO: Swing High ve Swing Low bulma
    #Swingleri etraftaki kaç muma göre arayacağıma karar vermem lazım, onu da range parametresiyle ayarlarım,
    #ilerde belki modele feedleyeceğim zaman bikaç rangede buldurur ve pcaini aldırırım
    def find_swings(self,range):
        for index,row in self.data.iterrows():
            print(candlestick)

        
    #TODO: Support ve Resistance Çizme
    

    #TODO: Trend Çizme