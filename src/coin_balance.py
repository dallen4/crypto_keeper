
class CoinBalance:
    def __init__(self, coin, amount, amountUsd):
        self.coin = coin
        self.amount = amount
        self.amountUsd = amountUsd

    def __str__(self):
        summary = str(self.coin) + '\t' + str(self.amount) + '\t$' + str(self.amountUsd)
        return summary
