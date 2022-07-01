import re
from statistics import mode
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas_datareader as web 
import datetime as dt
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense, Dropout, LSTM
import view
import test
import LSTM
import time
import investpy

app = dash.Dash()
server = app.server

#Build model
app.layout = html.Div(
    id = 'app',
    children = [
        view.header(),
        view.create_body_view(),
    ],
)

#update view

@app.callback(
    Output('loading-output-2', 'children'),
    Input('btnSearch', 'n_clicks'),
    State('edtCompanyCode', 'value')
)
def updateGraph(n_clicks, value):
    if n_clicks > 0:
        try:
            train_start = dt.datetime(2015, 1,1)
            train_end = dt.datetime(2022, 1,1 )
            data = investpy.get_stock_historical_data(stock=value,
                                country='vietnam',
                                from_date=train_start.strftime("%d/%m/%Y"),
                                to_date=train_end.strftime("%d/%m/%Y"))

            model = LSTM.getModel(data);

            #Load test data
            test_start = dt.datetime(2022,1,1)
            test_end = dt.datetime.now()

            # test_data = web.DataReader(value, 'yahoo', test_start, test_end)
            test_data = investpy.get_stock_historical_data(stock=value,
                                country='vietnam',
                                from_date=test_start.strftime("%d/%m/%Y"),
                                to_date=test_end.strftime("%d/%m/%Y"))
            
            print(test_data)

            actual_prices = test_data['Close'].values

            predicted_prices = LSTM.predictTestData(data = data, model=model, test_data= test_data)

            # predicted_prices2 = XGBoost.predictTestData(model=model, test_data= test_data)
            # predicted_prices3 = RNN.predictTestData(model=model, test_data= test_data)
            
            return view.getGraph(test_data, actual_prices, predicted_prices);
        except:
            return 'Khong tim thay ma chung khoan';


if __name__=='__main__':
    app.run_server(debug=True)


#https://github.com/bcmi/stock-price-prediction/blob/master/%E5%88%98%E6%80%9D%E8%BE%B0/XGBoost.py