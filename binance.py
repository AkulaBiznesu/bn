import requests
import csv
import sqlite3

def fetch_binance_data(symbol, interval):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}"
    response = requests.get(url)
    data = response.json()
    return data

def save_data_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_volume', 'count', 'taker_buy_volume', 'taker_buy_quote_volume', 'ignore'])
        writer.writerows(data)

def save_data_to_database(data, table_name:str):
    conn = sqlite3.connect('binance_data.db')
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (open_time INTEGER, open REAL, high REAL, low REAL, close REAL, volume REAL, close_time REAL, quote_volume REAL, count REAL, taker_buy_volume REAL, taker_buy_quote_volume REAL, ignore REAL)")
    cursor.executemany(f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

def main():
    symbol = input('provide symbol like (`BTCUSDT, ETHUSDT, etc.): ')
    interval = input('desired interval (e.g., 1d, 4h, 1h): ')                         
    data = fetch_binance_data(symbol, interval)
    save_data_to_csv(data, f'{symbol}_{interval}.csv')
    save_data_to_database(data, f'{symbol}_{interval}')

if __name__ == '__main__':
    main()
