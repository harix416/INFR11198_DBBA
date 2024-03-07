import random

class RandomTrader:
    def __init__(self, balance_gbp, balance_btc):
        self.balance_gbp = balance_gbp
        self.balance_btc = balance_btc
        self.is_position_open = False
    
    def decide_trade(self, price_history):
        now_price = price_history[-1]
        # Randomly decide whether to buy or sell
        trade_action = random.choice(['buy', 'sell'])
        
        # Execute the trade if there is balance available
        if trade_action == 'buy' and self.balance_gbp > 0:
            self.buy_btc(now_price)  # Assuming a fixed price for simplicity
        elif trade_action == 'sell' and self.balance_btc > 0:
            self.sell_btc(now_price)  # Assuming a fixed price for simplicity
    
    def buy_btc(self, price):
        # Buy as much BTC as possible with the available GBP balance
        btc_to_buy = self.balance_gbp / price
        self.balance_btc += btc_to_buy
        self.balance_gbp = 0
        self.is_position_open = True

    def sell_btc(self, price):
        # Sell all BTC and convert it to GBP
        gbp_to_get = self.balance_btc * price
        self.balance_gbp += gbp_to_get
        self.balance_btc = 0
        self.is_position_open = False

    def get_balance(self):
        return self.balance_gbp, self.balance_btc

price_history = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]

# Example usage
trader = RandomTrader(balance_gbp=1000, balance_btc=2)

# Simulate a trading day
trader.decide_trade(price_history)

# Get the updated balances
print(trader.get_balance())
