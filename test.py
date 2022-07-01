# import os
# import numpy as np
# import pandas as pd
# import xgboost as xgb
# import matplotlib.pyplot as plt
# from xgboost import plot_importance, plot_tree
# from sklearn.metrics import mean_squared_error
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.model_selection import train_test_split, GridSearchCV
# import pandas_datareader as web 
# import datetime as dt


# # Chart drawing
# import plotly as py
# import plotly.io as pio
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

# # # Mute sklearn warnings
# # from warnings import simplefilter
# # simplefilter(action='ignore', category=FutureWarning)
# # simplefilter(action='ignore', category=DeprecationWarning)

# # # Show charts when running kernel
# # init_notebook_mode(connected=True)

# # # Change default background color for all visualizations
# # layout=go.Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(250,250,250,0.8)')
# # fig = go.Figure(layout=layout)
# # templated_fig = pio.to_templated(fig)
# # pio.templates['my_template'] = templated_fig.layout.template
# # pio.templates.default = 'my_template'


# start = dt.datetime(2015, 1,1)
# end = dt.datetime(2022, 1,1 )

# #load data
# company = 'META'
# df = web.DataReader(company, 'yahoo', start, end)

# df['Date'] = df.index;
# df.index = range(len(df))

# df_close = df[['Date', 'Close']].copy()
# df_close = df_close.set_index('Date')


# df['EMA_9'] = df['Close'].ewm(9).mean().shift()
# df['SMA_5'] = df['Close'].rolling(5).mean().shift()
# df['SMA_10'] = df['Close'].rolling(10).mean().shift()
# df['SMA_15'] = df['Close'].rolling(15).mean().shift()
# df['SMA_30'] = df['Close'].rolling(30).mean().shift()

# # fig = go.Figure()
# # fig.add_trace(go.Scatter(x=df.Date, y=df.EMA_9, name='EMA 9'))
# # fig.add_trace(go.Scatter(x=df.Date, y=df.SMA_5, name='SMA 5'))
# # fig.add_trace(go.Scatter(x=df.Date, y=df.SMA_10, name='SMA 10'))
# # fig.add_trace(go.Scatter(x=df.Date, y=df.SMA_15, name='SMA 15'))
# # fig.add_trace(go.Scatter(x=df.Date, y=df.SMA_30, name='SMA 30'))
# # fig.add_trace(go.Scatter(x=df.Date, y=df.Close, name='Close', opacity=0.2))
# # fig.show()

# def relative_strength_idx(df, n=14):
#     close = df['Close']
#     delta = close.diff()
#     delta = delta[1:]
#     pricesUp = delta.copy()
#     pricesDown = delta.copy()
#     pricesUp[pricesUp < 0] = 0
#     pricesDown[pricesDown > 0] = 0
#     rollUp = pricesUp.rolling(n).mean()
#     rollDown = pricesDown.abs().rolling(n).mean()
#     rs = rollUp / rollDown
#     rsi = 100.0 - (100.0 / (1.0 + rs))
#     return rsi

# df['RSI'] = relative_strength_idx(df).fillna(0)

# # fig = go.Figure(go.Scatter(x=df.Date, y=df.RSI, name='RSI'))
# # fig.show()

# EMA_12 = pd.Series(df['Close'].ewm(span=12, min_periods=12).mean())
# EMA_26 = pd.Series(df['Close'].ewm(span=26, min_periods=26).mean())
# df['MACD'] = pd.Series(EMA_12 - EMA_26)
# df['MACD_signal'] = pd.Series(df.MACD.ewm(span=9, min_periods=9).mean())

# fig = make_subplots(rows=2, cols=1)
# fig.add_trace(go.Scatter(x=df.Date, y=df.Close, name='Close'), row=1, col=1)
# fig.add_trace(go.Scatter(x=df.Date, y=EMA_12, name='EMA 12'), row=1, col=1)
# fig.add_trace(go.Scatter(x=df.Date, y=EMA_26, name='EMA 26'), row=1, col=1)
# fig.add_trace(go.Scatter(x=df.Date, y=df['MACD'], name='MACD'), row=2, col=1)
# fig.add_trace(go.Scatter(x=df.Date, y=df['MACD_signal'], name='Signal line'), row=2, col=1)
# fig.show()