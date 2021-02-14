import time
import pandas as pd
from stockstats import StockDataFrame as Sdf
from dotenv import load_dotenv
load_dotenv()

from src.ftx_client import ftx_client
from src.coin import get_coin, get_coin_price, get_coin_volume
from src.coin_balance import CoinBalance
from src.account import get_balances, get_balance
from src.orders import buy_coin, sell_coin
from src.constants import DOGE_TICKER, USD, DOGE, ETH_TICKER, BTC_TICKER

convert_path = 'otc/quotes'

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

    if trade_signal == 2:
        print('BUY')
    elif trade_signal == 1:
        print('SOFT BUY')
    elif trade_signal == 0:
        print('HOLD')
    elif trade_signal == -1:
        print('SOFT SELL')
    elif trade_signal == -2:
        print('SELL')

    return (ts, trade_signal, last_rsi, advice[-1])

def run_trade_cycle(ticker):
    balances = get_balances()
    usd_balance = balances[USD]

    max_buy = 0

    if usd_balance.amountUsd > 20:
        max_buy = 20

    (timestamp, signal, rsi, macd_advice) = get_trade_signal_for_coin(ticker)
    coin_price = get_coin_price(ticker)

    print(ticker + ' ' + timestamp)
    print(coin_price)
    print('RSI: ' + str(rsi))
    print('MACD Signal: ' + macd_advice)
    print(signal)

    if signal == 2:
        if max_buy > 0:
            amount_to_buy = max_buy / coin_price
            buy_coin(ticker, amount_to_buy)
            print('BOUGHT ' + str(amount_to_buy) + ' ' + ticker)
        else:
            print('MISSED BUY')
    elif signal == -2:
        coin_balance = balances[ticker.split('/')[0]]
        amount_to_sell = coin_balance.amount * .25
        sell_coin(ticker, amount_to_sell)
        print('SOLD ' + str(amount_to_sell) + ' ' + ticker)

    print('------------------------')

run = True

while run == True:

    tickers = [DOGE_TICKER, ETH_TICKER, BTC_TICKER]

    run_trade_cycle(DOGE_TICKER)

    time.sleep(60)
    # break
