
import datetime as dt
import pandas_datareader as web 
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_boston
from sklearn.preprocessing import LabelEncoder

scaler = MinMaxScaler(feature_range=(0, 1))
prediction_days = 60;


def getModel(data):
    # prepare data
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1,1))

    x_train = []
    y_train = []

    for x in range(prediction_days, len(scaled_data)):
        x_train.append(scaled_data[x - prediction_days: x, 0])
        y_train.append(scaled_data[x, 0])
    x_train, y_train = np.array(x_train), np.array(y_train)
    #x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    le = LabelEncoder()
    y_train = le.fit_transform(y_train)

    #Build model

    model = XGBClassifier()
    model.fit(x_train, y_train)
    return model

def predictTestData(data, model, test_data):
    total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)

    model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days: ].values
    model_inputs = model_inputs.reshape(-1, 1)
    model_inputs = scaler.transform(model_inputs)
 
    #Make prediction on test data

    x_test = []
    for x in range(prediction_days, len(model_inputs)):
        x_test.append(model_inputs[x - prediction_days: x, 0])
    x_test = np.array(x_test)
    
    predicted_prices = model.predict(x_test)
    real_data = [model_inputs[len(model_inputs) - prediction_days: len(model_inputs), 0]]
    real_data = np.array(real_data);
    predicted_next_timeframe = model.predict(real_data);
    predicted_next_timeframe = np.reshape(predicted_next_timeframe, (1,1))
    return predicted_prices, predicted_next_timeframe;