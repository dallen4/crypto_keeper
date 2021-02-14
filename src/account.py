from .ftx_client import ftx_client
from .coin_balance import CoinBalance

def get_balances():
    balances_data = ftx_client.fetch_balance()
    balances_data = balances_data['info']['result']
    balances = {}

    for coin in balances_data:
        curr_balance = CoinBalance(coin['coin'], coin['total'], coin['usdValue'])
        balances[coin['coin']] = curr_balance

    return balances

def get_balance(coin):
    balances = get_balances()
    return balances[coin]
