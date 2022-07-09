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
import body
import body1
import body2
import RNN
import XGBoost

app = dash.Dash()
server = app.server

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
            train_end = dt.datetime(2020, 1,1 )
            data = investpy.get_stock_historical_data(stock=value,
                                country='vietnam',
                                from_date=train_start.strftime("%d/%m/%Y"),
                                to_date=train_end.strftime("%d/%m/%Y"))

            model = LSTM.getModel(data);
            model1 = RNN.getModel(data);
            model2 = XGBoost.getModel(data);

            #Load test data
            test_start = dt.datetime(2020,1,1)
            test_end = dt.datetime.now()

            test_data = investpy.get_stock_historical_data(stock=value,
                                country='vietnam',
                                from_date=test_start.strftime("%d/%m/%Y"),
                                to_date=test_end.strftime("%d/%m/%Y"))
            predicted_prices, predicted_next_timeframe = LSTM.predictTestData(data = data, model=model, test_data= test_data)
            predicted_prices1, predicted_next_timeframe1 = RNN.predictTestData(data = data, model=model1, test_data= test_data)
            predicted_prices2, predicted_next_timeframe2 = XGBoost.predictTestData(data = data, model=model2, test_data= test_data)
            indicator_data = [data, test_data]
            indicator_data = pd.concat(indicator_data)

            return html.Div(
                children = [
                    body.getLstmView(data, test_data, predicted_prices, predicted_next_timeframe),
                    body1.getLstmView(data, test_data, predicted_prices1, predicted_next_timeframe1),
                    body2.getLstmView(data, test_data, predicted_prices2, predicted_next_timeframe2),
                    body.getIndicatorView(indicator_data)
                ]
            );
        except Exception as e: 
            return e;


if __name__=='__main__':
    app.run_server(debug=True)
