import time
from dotenv import load_dotenv
from rich import print
from rich.panel import Panel
from rich.layout import Layout
from rich.padding import Padding
load_dotenv()

from src.account import get_balances
from src.trade import run_trade_cycle
from src.constants import DOGE_TICKER, USD, DOGE, ETH_TICKER, BTC_TICKER

run = True
balance_list = []

def check_coins():
    (balances, total_balance) = get_balances()

    balance_list.append(total_balance)
    account_output = '[bold]Total Account Balance:[/bold] [blue]' + str(total_balance) + '[/blue]'

    diff_since_start = total_balance - balance_list[0]

    color = 'green'

    if diff_since_start < 0:
        color = 'red'

    account_output += '\n[bold]Balance Change Since Start:[/bold] [' + color + ']' + str(diff_since_start) + '[/' + color + ']'

    account_panel = Panel(account_output)

    usd_balance = balances[USD]

    max_buy = 0

    if usd_balance.amountUsd > 20:
        max_buy = 20

    tickers = [DOGE_TICKER, ETH_TICKER, BTC_TICKER]
    summaries = []

    for ticker in tickers:
        trade_summary = run_trade_cycle(ticker, max_buy)
        summaries.append(trade_summary)

    cycle_layout = Layout()

    cycle_layout.split(
        Layout(account_panel, name='top'),
        Layout(name='bottom')
    )

    cycle_layout['top'].size = 5
    cycle_layout['bottom'].size = 10

    cycle_layout['bottom'].split(
        Layout(Panel(Padding(summaries[0], 1))),
        Layout(Panel(Padding(summaries[1], 1))),
        Layout(Panel(Padding(summaries[2], 1))),
        direction='horizontal'
    )
    print(cycle_layout)

def main():
    while run == True:
        check_coins()
        time.sleep(60)


if __name__ == '__main__':
    main()
