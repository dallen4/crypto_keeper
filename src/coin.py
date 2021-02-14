from src.ftx_client import ftx_client

def get_coin(ticker):
    return ftx_client.fetch_ticker(ticker)

def get_coin_price(ticker):
    data = get_coin(ticker)
    return data['info']['price']

def get_coin_volume(ticker):
    data = get_coin(ticker)
    return data['baseVolume']
