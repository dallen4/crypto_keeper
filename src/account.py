from src.ftx_client import ftx_client
from src.coin_balance import CoinBalance

def get_balances():
    balances_data = ftx_client.fetch_balance()
    balances_data = balances_data['info']['result']
    balances = {}
    total_balance = 0

    for coin in balances_data:
        symbol = coin['coin']
        curr_balance = CoinBalance(symbol, coin['total'], coin['usdValue'])
        balances[symbol] = curr_balance
        total_balance += curr_balance.amountUsd

    return (balances, total_balance)

def get_balance(coin):
    (balances) = get_balances()
    return balances[coin]
