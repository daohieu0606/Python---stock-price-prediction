from turtle import color
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
import numpy as np


def getLstmView(train_data, test_data, predicted_prices, predicted_next_timeframe):
    # Create subplots and mention plot grid size
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)

    fig.add_trace(
        go.Scatter(x=train_data.index, y=train_data['Close'], name ='train_data',mode = 'lines'),
        row=1, 
        col=1);
    fig.add_trace(
        go.Scatter(x=test_data.index, y=test_data['Close'], name ='test_data',mode = 'lines'),
        row=1, 
        col=1);
    fig.add_trace(
        go.Scatter(x=test_data.index, y=predicted_prices, name ='predicted_prices',mode = 'lines'),
        row=1, 
        col=1);
    # Do not show OHLC's rangeslider plot 
    fig.update(layout_xaxis_rangeslider_visible=False)

    #remove date gaps
    date_gaps = [date for date 
                    in pd.date_range(start = train_data.index[0], end = test_data.index[-1]) 
                    if (date not in train_data.index) and (date not in test_data.index)]
    fig.update_xaxes(rangebreaks = [dict(values = date_gaps)])

    # Make it pretty
    layout = go.Layout(
        plot_bgcolor='#efefef',
        # Font Families
        font_family='Monospace',
        font_color='#000000',
        font_size=20,
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        )
    )

    # Update options and show plot
    fig.update_layout(layout)
    fig.update_layout(height=500)

    statement = "Predicted next timeframe price: " + str(predicted_next_timeframe[0][0]);
    return html.Div(
        children = [
            html.H1(
                children= "1. LSTM",
                style={'margin-left':'50px'}),
            html.H1(
                children= statement,
                style={'text-align':'center'}),
            dcc.Graph(
                id="Predicted Data",
                figure= fig,
            ),
        ]
    );


def getIndicatorView(df):
    return html.Div(
        children = [
            html.H1(
                children= "2. Technial Indicator (MACD & Bollinger Bands)",
                style={'margin-left':'50px'}),
            dcc.Graph(
                id="macd",
                figure= macdView(df),
            ),
        ]
    );

def macdView(df):
    # # Calculate MACD values using the pandas_ta library
    # df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
    # Get the 26-day EMA of the closing price
    k = df['Close'].ewm(span=12, adjust=False, min_periods=12).mean()
    # Get the 12-day EMA of the closing price
    d = df['Close'].ewm(span=26, adjust=False, min_periods=26).mean()
    # Subtract the 26-day EMA from the 12-Day EMA to get the MACD
    macd = k - d
    # Get the 9-Day EMA of the MACD for the Trigger line
    macd_s = macd.ewm(span=9, adjust=False, min_periods=9).mean()
    # Calculate the difference between the MACD - Trigger for the Convergence/Divergence value
    macd_h = macd - macd_s
    # Add all of our new values for the MACD to the dataframe
    df['macd'] = df.index.map(macd)
    df['macd_h'] = df.index.map(macd_h)
    df['macd_s'] = df.index.map(macd_s)
    # View our data
    pd.set_option("display.max_columns", None)

    # Construct a 2 x 1 Plotly figure
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
    # # price Line
    # fig.append_trace(
    #     go.Scatter(
    #         x=df.index,
    #         y=df['Open'],
    #         line=dict(color='#ff9900', width=1),
    #         name='open',
    #         # showlegend=False,
    #         legendgroup='1',
    #     ), row=1, col=1
    # )
    # Candlestick chart for pricing
    candy_view = go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            increasing_line_color='#ff9900',
            decreasing_line_color='black',
            showlegend=False
        );

    fig.append_trace(candy_view, row=1, col=1)

    # Fast Signal (%k)
    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['macd'],
            line=dict(color='#ff9900', width=2),
            name='macd',
            # showlegend=False,
            legendgroup='2',
        ), row=2, col=1
    )
    # Slow signal (%d)
    fig.append_trace(
        go.Scatter(
            x=df.index,
            y=df['macd_s'],
            line=dict(color='#000000', width=2),
            # showlegend=False,
            legendgroup='2',
            name='signal'
        ), row=2, col=1
    )
    # Colorize the histogram values
    colors = np.where(df['macd_h'] < 0, '#000', '#ff9900')
    # Plot the histogram
    fig.append_trace(
        go.Bar(
            x=df.index,
            y=df['macd_h'],
            name='histogram',
            marker_color=colors,
        ), row=2, col=1
    )

    add_bollinger_band(fig=fig, df=df);
    # add_ma_line(fig=fig, df=df);

    # Make it pretty
    layout = go.Layout(
        plot_bgcolor='#efefef',
        # Font Families
        font_family='Monospace',
        font_color='#000000',
        font_size=20,
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        )
    )

    #remove date gaps
    date_gaps = [date for date 
                    in pd.date_range(start = df.index[0], end = df.index[-1]) 
                    if (date not in df.index) and (date not in df.index)]
    fig.update_xaxes(rangebreaks = [dict(values = date_gaps)])


    # Update options and show plot
    fig.update_layout(layout)
    fig.update_layout(height=800)
    return fig;


def bollingerView(df):
    WINDOW = 30
    df['sma'] = df['Close'].rolling(WINDOW).mean()
    df['std'] = df['Close'].rolling(WINDOW).std(ddof = 0)
        
    # Create subplots with 2 rows; top for candlestick price, and bottom for bar volume
    fig = make_subplots(rows = 2, cols = 1, shared_xaxes = True, subplot_titles = ('IBM', 'Volume'), vertical_spacing = 0.1, row_width = [0.2, 0.7])

    # ----------------
    # Candlestick Plot
    fig.add_trace(go.Candlestick(x = df.index,
                                open = df['Open'],
                                high = df['High'],
                                low = df['Low'],
                                close = df['Close'], showlegend=False,
                                name = 'candlestick'),
                row = 1, col = 1)

    # Moving Average
    fig.add_trace(go.Scatter(x = df.index,
                            y = df['sma'],
                            line_color = 'black',
                            name = 'sma'),
                row = 1, col = 1)

    # Upper Bound
    fig.add_trace(go.Scatter(x = df.index,
                            y = df['sma'] + (df['std'] * 2),
                            line_color = 'gray',
                            line = {'dash': 'dash'},
                            name = 'upper band',
                            opacity = 0.5),
                row = 1, col = 1)

    # Lower Bound fill in between with parameter 'fill': 'tonexty'
    fig.add_trace(go.Scatter(x = df.index,
                            y = df['sma'] - (df['std'] * 2),
                            line_color = 'gray',
                            line = {'dash': 'dash'},
                            fill = 'tonexty',
                            name = 'lower band',
                            opacity = 0.5),
                row = 1, col = 1)


    # ----------------
    # Volume Plot
    fig.add_trace(go.Bar(x = df.index, y = df['Volume'], showlegend=False), 
                row = 2, col = 1)

    # Remove range slider; (short time frame)
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(height=800)

    #remove date gaps
    date_gaps = [date for date 
                    in pd.date_range(start = df.index[0], end = df.index[-1]) 
                    if (date not in df.index) and (date not in df.index)]
    fig.update_xaxes(rangebreaks = [dict(values = date_gaps)])

    return fig;

def add_bollinger_band(fig, df):
    WINDOW = 30
    df['sma'] = df['Close'].rolling(WINDOW).mean()
    df['std'] = df['Close'].rolling(WINDOW).std(ddof = 0)

    # Moving Average
    fig.add_trace(go.Scatter(x = df.index,
                            y = df['sma'],
                            line_color = 'black',
                            name = 'sma'),
                row = 1, col = 1)

    # Upper Bound
    fig.add_trace(go.Scatter(x = df.index,
                            y = df['sma'] + (df['std'] * 2),
                            line_color = 'gray',
                            line = {'dash': 'dash'},
                            name = 'upper band',
                            opacity = 0.5),
                row = 1, col = 1)

    # Lower Bound fill in between with parameter 'fill': 'tonexty'
    fig.add_trace(go.Scatter(x = df.index,
                            y = df['sma'] - (df['std'] * 2),
                            line_color = 'gray',
                            line = {'dash': 'dash'},
                            fill = 'tonexty',
                            name = 'lower band',
                            opacity = 0.5),
                row = 1, col = 1)

def add_ma_line(fig, df):
    df['SMA_9'] = df['Close'].rolling(9).mean().shift()
    df['SMA_20'] = df['Close'].rolling(20).mean().shift()
    df['SMA_200'] = df['Close'].rolling(200).mean().shift()

    fig.add_trace(go.Scatter(x = df.index,
                            y = df['SMA_9'],
                            line_color = 'blue',
                            name = 'ma9'),
                row = 1, col = 1)
    fig.add_trace(go.Scatter(x = df.index,
                            y = df['SMA_20'],
                            line_color = 'red',
                            name = 'ma20'),
                row = 1, col = 1)
    fig.add_trace(go.Scatter(x = df.index,
                            y = df['SMA_200'],
                            line_color = 'purple',
                            name = 'ma200'),
                row = 1, col = 1)