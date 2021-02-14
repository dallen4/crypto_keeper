import time
from dotenv import load_dotenv
load_dotenv()

from src.coin import get_coin_price, get_trade_signal_for_coin
from src.account import get_balances
from src.orders import buy_coin, sell_coin
from src.constants import DOGE_TICKER, USD, DOGE, ETH_TICKER, BTC_TICKER

convert_path = 'otc/quotes'

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
