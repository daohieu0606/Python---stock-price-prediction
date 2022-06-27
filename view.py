import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

def inputCompanyView():
    view = dcc.Input(
        id='edtCompanyCode',
        placeholder = 'Enter Company Code'
    )

    return view;

def dropdown_select_method():
    view = dcc.Dropdown( 
        id = 'dropdown',
        options = [
            {'label':'Google', 'value':'GOOG' },
            {'label': 'Apple', 'value':'AAPL'},
            {'label': 'Amazon', 'value':'AMZN'},
            ],
        value = 'GOOGL',
        className='method-dropdown'
    )

    return view;

def button_search_view():
    view = html.Button('Search',
        id='btnSearch', 
        n_clicks=0, 
        );

    return view;

def header():
    view = html.Div(
            className="header",
            children = [
                search_bar(),
            ]
        );

    return view;

def search_bar():
    view = html.Div(
        className="topnav",
        children = [
            inputCompanyView(),
            button_search_view()
        ]
    );

    return view;

def create_body_view():
    view = html.Div(
            className = 'content',
            children = [
                dcc.Loading(
                    id="pgLoading",
                    className ='center-loading',
                    children=[html.Div([html.Div(id="loading-output-2")])],
                    type="circle",
                )
                
            ]
        );
    return view;

def getGraph(test_data, actual_prices, predicted_prices):
    fig = dcc.Graph(
        id="Predicted Data",
        figure={
            'data': [
                {
                    'x': test_data.index, 
                    'y': actual_prices, 
                    'type': 'line', 
                    'name': 'Actual Price'
                },
                {
                    'x': test_data.index, 
                    'y': predicted_prices, 
                    'type': 'line', 
                    'name': 'Predicted Price'
                },
                # go.Candlestick(x=test_data.index,
                #     open=test_data['Open'],
                #     high=test_data['High'],
                #     low=test_data['Low'],
                #     close=test_data['Close']
                #     )
            ],
            "layout":go.Layout(
                title='scatter plot',
                xaxis={'title':'Date'},
                yaxis={'title':'Price'}
            )
        }
    )

    return fig;
