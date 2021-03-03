# Contains helper functions for your apps!
from os import listdir, remove
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import pandas as pd
from os import listdir, remove
import pickle
from time import sleep

from helper_functions_copy import * # this statement imports all functions from your helper_functions file!

#Check
check_for_and_del_io_files('currency_pair.txt')
check_for_and_del_io_files('currency_pair_history.csv')
check_for_and_del_io_files('trade_order.p')


# Make a Dash app!
app = dash.Dash(__name__)

# Define the layout.
app.layout = html.Div([

    # Section title
    html.H1("Section 1: Fetch & Display exchange rate historical data"),

    # Currency pair text input, within its own div.
    html.Div(
        [
            "Input Currency: ",
            # Your text input object goes here:
            dcc.Input(id = 'currency-pair', value = 'AUDCAD',  type = 'text')

        ],
        # Style it so that the submit button appears beside the input.
        style={'display': 'inline-block'}
    ),
    # Submit button:
    html.Button('Submit', id = 'submit-button', n_clicks = 0),
    # Line break
    html.Br(),
    # Div to hold the initial instructions and the updated info once submit is pressed
    html.Div(id='output-div', children='Enter a currency code and press "submit"'),
    html.Div([
        # Candlestick graph goes here:

        dcc.Graph(id='candlestick-graph')
    ]),
    # Another line break
    html.Br(),
    # Section title
    html.H1("Section 2: Make a Trade"),
    # Div to confirm what trade was made
    html.Div(id='trade-output'),
    # Radio items to select buy or sell
    dcc.RadioItems(id='action',
        options=[
            {'label': 'Buy', 'value': 'BUY'},
            {'label': 'Sell', 'value': 'SELL'},
            ],
    ),
    # Text input for the currency pair to be traded
    dcc.Input(id='trade_currency',type='text')
             ,
    # Numeric input for the trade amount
    dcc.Input(id='trade_amt',type='number')
             ,
    # Submit button for the trade
    html.Button('Trade', id='trade_submit', n_clicks=0)

])

# Callback for what to do when submit-button is pressed
@app.callback(
    [ # there's more than one output here, so you have to use square brackets to pass it in as an array.
    Output('output-div','children'),Output('candlestick-graph','figure')
    ],[Input('submit-button', 'n_clicks')]
    ,[State('currency-pair', 'value')]
)
def update_candlestick_graph(n_clicks, value): # n_clicks doesn't get used, we only include it for the dependency.
    # Now we're going to save the value of currency-input as a text file.
    print(value, n_clicks)
    with open("currency_pair.txt", "w") as f:
        f.write(value)
    # Wait until ibkr_app runs the query and saves the historical prices csv
    while 'currency_pair_history.csv' not in listdir():
        sleep(0.1)
        # Read in the historical prices
    read_history_csv = pd.read_csv('currency_pair_history.csv')
    # Remove the file 'currency_pair_history.csv'
    os.remove("currency_pair_history.csv")

    # Make the candlestick figure
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=read_history_csv['date'],
                open=read_history_csv['open'],
                high=read_history_csv['high'],
                low=read_history_csv['low'],
                close=read_history_csv['close']
            )
        ]
    )
    # Give the candlestick figure a title
    fig.update_layout(title=value)

    # Return your updated text to currency-output, and the figure to candlestick-graph outputs
    return ('Submitted query for ' + value), fig

# Callback for what to do when trade-button is pressed
@app.callback(
    Output('trade-output', 'children'),
    [Input('trade_submit', 'n_clicks')],
    [State('action', 'value'), State('trade_currency', 'value'),
     State('trade_amt', 'value')],
    # We DON'T want to start executing trades just because n_clicks was initialized to 0!!!
    prevent_initial_call=True
)
def trade(n_clicks, action, trade_currency, trade_amt): # Still don't use n_clicks, but we need the dependency
    msg = str(action)+' ' + str(trade_currency) + ' ' + str(trade_amt)
    # Make the message that we want to send back to trade-output
    trade_order = {
        "action": action,
        "trade_currency": trade_currency,
        "trade_amt": trade_amt
    }
    # Make our trade_order object -- a DICTIONARY.

    # Dump trade_order as a pickle object to a file connection opened with write-in-binary ("wb") permission:
    pickle.dump(trade_order, open("trade_order.p", "wb"))

    # Return the message, which goes to the trade-output div's "children" attribute.
    return msg

# Run it!
if __name__ == '__main__':
    app.run_server(debug=True)
