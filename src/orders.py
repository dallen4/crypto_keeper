from src.ftx_client import ftx_client

def buy_coin(symbol, amount):
    order = ftx_client.create_order(symbol, 'market', 'buy', amount)
    print(order)

def sell_coin(symbol, amount):
    order = ftx_client.create_order(symbol, 'market', 'sell', amount)
    print(order)
