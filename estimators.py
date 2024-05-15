class Estimator:
    #X is a pd dataframe of an assets data
    def __init__(self,X):
        self.y = X[1:]
    def get_y(self):
        return self.y[["Open","High","Low","Close"]]
    