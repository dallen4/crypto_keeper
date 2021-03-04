import time
import pandas as pd
from stockstats import StockDataFrame as Sdf
from src.ftx_client import ftx_client

def get_coin(ticker):
    return ftx_client.fetch_ticker(ticker)

def get_coin_price(ticker):
    data = get_coin(ticker)
    return data['info']['price']

def get_coin_volume(ticker):
    data = get_coin(ticker)
    return data['baseVolume']

def get_trade_signal_for_coin(ticker):
    # fetch historical data
    data = ftx_client.fetch_ohlcv(ticker, '1m')

    # cast timestamps to readable format
    data = [[ftx_client.iso8601(candle[0])] + candle[1:] for candle in data]

    # parse data into DataFrame
    header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    coinFrame = pd.DataFrame(data, columns=header)

    # impl SDF wrapper to provide more functionality
    stock_structured_data = Sdf.retype(coinFrame)

    # calculate RSI
    stock_structured_data['rsi_14']
    last_rsi = stock_structured_data['rsi_14'].iloc[-1]

    # calculate macd and retrieve macd line and signal line
    macd = stock_structured_data['macd']
    macd_signal = stock_structured_data['macds']
    timestamps = stock_structured_data['timestamp']
    advice = []

    data_length = len(macd_signal)
    ts = timestamps[data_length - 1]

    for index in range(data_length - 20, data_length):
        if macd[index] > macd_signal[index] and macd[index - 1] <= macd_signal[index - 1]:
            advice.append('BUY')
        elif macd[index] < macd_signal[index] and macd[index - 1] >= macd_signal[index - 1]:
            advice.append('SELL')
        else:
            advice.append('HOLD')

    # positive = buy, negative = sell
    trade_signal = 0

    if last_rsi < 30:
        trade_signal += 1
    elif last_rsi > 70:
        trade_signal -= 1

    if advice[-1] == 'BUY':
        trade_signal += 1
    elif advice[-1] == 'SELL':
        trade_signal -= 1

    return (ts, trade_signal, last_rsi, advice[-1])
