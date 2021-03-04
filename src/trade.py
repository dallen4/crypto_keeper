from src.coin import get_coin_price, get_trade_signal_for_coin
from src.orders import buy_coin, sell_coin
from src.account import get_balance

signal_map = {
    2: '[green]BUY[/green]',
    1: '[blue]SOFT BUY[/blue]',
    0: 'HOLD',
    -1: '[yellow]SOFT SELL[/yellow]',
    -2: '[orange]SELL[/orange]'
}

def format_signal_msg(signal):
    signal_txt = signal_map[signal]
    return f'[bold]{signal_txt} ({signal})[/bold]'


def run_trade_cycle(ticker, max_buy):
    (timestamp, signal, rsi, macd_advice) = get_trade_signal_for_coin(ticker)
    coin_price = get_coin_price(ticker)

    summary = ticker + ' ' + timestamp
    summary += f'\n{coin_price}'
    summary += f'\nRSI: {rsi}'
    summary += f'\nMACD Signal: {macd_advice}'
    summary += f'\n{format_signal_msg(signal)}'

    if signal == 2:
        if max_buy > 0:
            amount_to_buy = max_buy / coin_price
            buy_coin(ticker, amount_to_buy)
            summary += '\nBOUGHT ' + str(amount_to_buy) + ' ' + ticker
        else:
            summary += '\nMISSED BUY'
    elif signal == -2:
        coin_balance = get_balance(ticker.split('/')[0])
        amount_to_sell = coin_balance.amount * .25
        sell_coin(ticker, amount_to_sell)
        summary += '\nSOLD ' + str(amount_to_sell) + ' ' + ticker

    return summary
