import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error,mean_absolute_error
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input

class Estimator:
    #X is a pd dataframe of an assets data
    def __init__(self,X):
        self.X=X
        self.y = X[1:]
        self.y = self.y[["Open","High","Low","Close"]]
    def get_x(self):
        return self.X
    def preprocessing(self):
        pass
    def get_y(self):
        return self.y

class LSTMDataPreprocessor:
    def __init__(self, p, mode,time_step=30):
        # Loading dataset
        dataset = pd.read_csv(p)
        
        # Converting timestamps to datetime
        dataset['Open Time'] = pd.to_datetime(dataset['Open Time'])
        dataset['Close Time'] = pd.to_datetime(dataset['Close Time'])

        # Extracting useful features from timestamps
        dataset['Hour'] = dataset['Open Time'].dt.hour
        dataset['Day'] = dataset['Open Time'].dt.day
        dataset['Month'] = dataset['Open Time'].dt.month
        dataset['Minute'] = dataset['Open Time'].dt.minute
        dataset["Year"] = dataset["Open Time"].dt.year
        # Define columns for X and y
        x_columns_to_scale = ["Volume", "Quote Asset Volume", "Number of Trades", "Taker Buy Volume", "Taker Buy Quote Asset Volume"]
        x_columns_no_scale = ["Hour", "Day", "Month", "Minute","Year"]
        y_columns = mode
        
        # Scaling the data
        self.X_scaler = MinMaxScaler()
        self.y_scaler = MinMaxScaler()
        
        self.X = self.preprocess(dataset, x_columns_to_scale, x_columns_no_scale, time_step, scaler=self.X_scaler)[0]
        self.y = self.preprocess(dataset[y_columns], time_step, scaler=self.y_scaler, scale=True)[0]

    def preprocess(self, data, columns_to_scale, columns_no_scale=None, time_step=30, scaler=None, scale=False):
        if scale:
            data_scaled = scaler.fit_transform(data)
            return self.create_sequences(data_scaled, time_step)
        
        # Scale only the selected columns
        data_scaled = scaler.fit_transform(data[columns_to_scale])
        
        # Concatenate scaled and non-scaled columns
        if columns_no_scale:
            data_no_scale = data[columns_no_scale].values
            data_combined = np.concatenate((data_scaled, data_no_scale), axis=1)
        else:
            data_combined = data_scaled

        return self.create_sequences(data_combined, time_step)

    def create_sequences(self, data, time_step):
        X, y = [], []
        for i in range(len(data) - time_step):
            X.append(data[i:(i + time_step), :])
            y.append(data[i + time_step, :])  # Assuming you want to predict all columns

        return np.array(X), np.array(y)

class LSTMModel:
    def __init__(self, data,time_steps,mode=["Close"]):
        self.time_steps = time_steps
        self.preprocessor = LSTMDataPreprocessor(data,mode,time_steps)
        self.input_shape, self.output_shape = self.preprocessor.X.shape[1:], self.preprocessor.y.shape[1:]
        self.X_train, self.X_test, self.y_train, self.y_test = self.train_test_split()
        self.model = self.build_model()

    def build_model(self):
        model = Sequential([
            Input(shape=self.input_shape),
            LSTM(64, return_sequences=True),
            LSTM(64),
            Dense(self.output_shape[0])
        ])
        model.compile(optimizer='adam', loss='mean_absolute_error')
        return model

    def train_test_split(self, test_size=0.2):
        return train_test_split(self.preprocessor.X, self.preprocessor.y, test_size=test_size, random_state=42)

    def train(self, epochs=10, batch_size=32):
        history = self.model.fit(self.X_train, self.y_train, validation_data=(self.X_test, self.y_test), epochs=epochs, batch_size=batch_size)
        return history

    def plot_learning_curve(self, history):
        plt.figure(figsize=(12, 6))
        plt.plot(history.history['loss'], label='Training Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.title('Learning Curve')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()

    def plot_real_vs_predicted(self):
        y_pred = self.model.predict(self.X_test)
        y_pred_rescaled = self.preprocessor.y_scaler.inverse_transform(y_pred)
        y_test_rescaled = self.preprocessor.y_scaler.inverse_transform(self.y_test)

        plt.figure(figsize=(12, 6))
        plt.plot(y_test_rescaled[:, 0], label='Real')
        plt.plot(y_pred_rescaled[:, 0], label='Predicted')
        plt.title('Real vs Predicted')
        plt.xlabel('Time Step')
        plt.ylabel('Value')
        plt.legend()
        plt.show()

class LinearRegression(Estimator):
    def __init__(self,X):
        super().__init__(X)
        self.model = Ridge()
        self.y = self.X["Close"].values
        self.X = self.X.drop(["Open","High","Low","Close","Open Time","Close Time","Index"],axis=1)
    def build_model_then_predict(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.33, random_state=42)
        self.model.fit(X_train,y_train)
        yhat = self.model.predict(X_test)
        return mean_absolute_error(yhat,y_test)

class NaiveEstimator(Estimator):
    def __init__(self,X):
        super().__init__(X)
        self.X = X
        self.y = X["Close"].shift(-1)
    def return_score(self):
    # Impute missing values with a strategy (e.g., mean)
        self.y.fillna(self.y.mean(), inplace=True)
        return mean_absolute_error(self.X["Close"], self.y)

df = pd.read_csv(r"D:\binanceapi\MarketData\LTCUSDT\LTCUSDT_15m.csv")
LinearModel = LinearRegression(df)
NaiveModel = NaiveEstimator(df)
print("Naive Model Error"+str(NaiveModel.return_score()))
print("Linear Mean Absolute Error"+str(LinearModel.build_model_then_predict()))