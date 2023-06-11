from flask import Flask, render_template, request
import requests
import sqlite3
import pandas as pd
import plotly.graph_objects as go

app = Flask(__name__)

# Task 1: Data Collection
def fetch_binance_data(symbol, interval):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}"
    response = requests.get(url)
    data = response.json()
    return data

def fetch_binance_symbols():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    data = response.json()
    symbols = [symbol['symbol'] for symbol in data['symbols']]
    return symbols

def save_data_to_database(data, table_name):
    conn = sqlite3.connect('binance_data.db')
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (open_time INTEGER, open REAL, high REAL, low REAL, close REAL, volume REAL, close_time REAL, quote_volume REAL, count REAL, taker_buy_volume REAL, taker_buy_quote_volume REAL, ignore REAL)")
    cursor.executemany(f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

# Task 2: Flask UI
def load_data_from_database(table_name):
    conn = sqlite3.connect('binance_data.db')
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (open_time INTEGER, open REAL, high REAL, low REAL, close REAL, volume REAL, close_time REAL, quote_volume REAL, count REAL, taker_buy_volume REAL, taker_buy_quote_volume REAL, ignore REAL)")
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    df = pd.DataFrame(data, columns=columns)
    conn.close()
    return df

def create_candlestick_chart(df):
    candlestick = go.Candlestick(x=df['open_time'], open=df['open'], high=df['high'], low=df['low'], close=df['close'])
    return candlestick

def create_pie_chart():
    pie_labels = ['BTCUSDT', 'ETHUSDT', 'DOGEUSDT', 'SHIBUSDT', 'XRPUSDT', 'BNBUSDT', 'ADAUSDT', 'WBTCUSDT', 'DASHUSDT', 'SOLUSDT']  
    pie_values = [fetch_binance_data(value, '1d')[5][1] for value in pie_labels]  
    pie = go.Pie(labels=pie_labels, values=pie_values)
    return pie

@app.route('/', methods=['GET', 'POST'])
def display_data():

    symbol_list = fetch_binance_symbols()
    interval_list = ['1s', '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1mo']

    if request.method == 'POST':
        # Get user input from the form
        symbol = request.form['symbol']
        interval = request.form['interval']

        # Fetch and save data to the database
        data = fetch_binance_data(symbol, interval)
        save_data_to_database(data, f'{symbol}_{interval}')

        # Load data from database
        df = load_data_from_database(f'{symbol}_{interval}')

        # Create charts
        candlestick = create_candlestick_chart(df)

        # Create the figure with both charts
        fig = go.Figure(data=[candlestick])

        # Convert the figure to HTML
        chart_html = fig.to_html(full_html=False, default_height=500)

        # return render_template('index.html', chart_html=chart_html)

        pie = create_pie_chart()
        figa = go.Figure(data=pie)
        chart_html_pie = figa.to_html(full_html=False, default_height=500)
        return render_template('index.html', chart_html_pie=chart_html_pie, chart_html=chart_html, symbol_list=symbol_list, interval_list=interval_list)
    return render_template('index.html', symbol_list=symbol_list, interval_list=interval_list)

if __name__ == '__main__':
    app.run(debug=True)
