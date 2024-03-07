class chartistAgent:
    def __init__(self, balance_gbp, balance_btc, open_position_subtypes, close_position_subtypes):
        self.balance_gbp = balance_gbp
        self.balance_btc = balance_btc

        # open_position_subtypes is 1 then rule 1 80% and rule 2 20%
        # open_position_subtypes is 2 then rule 1 20% and rule 2 80%
        self.open_position_subtypes = open_position_subtypes
        # close_position_subtypes is 1 then rule 1 80% and rule 2 20%
        # close_position_subtypes is 2 then rule 1 20% and rule 2 80%
        self.close_position_subtypes = close_position_subtypes

        self.is_open_position = False
        # self.is_close_position = False

        self.ema = None
    
    def get_balance(self):
        return self.balance_gbp, self.balance_btc
    
    def get_open_position_subtypes(self):
        return self.open_position_subtypes
    
    def get_close_position_subtypes(self):
        return self.close_position_subtypes
    
    def get_ema(self):
        return self.ema
    
    def buy_btc(self, price):
        self.balance_btc = self.balance_gbp / price
        self.balance_gbp = 0

    def sell_btc(self, price):
        self.balance_gbp = self.balance_btc * price
        self.balance_btc = 0

    def filtering_threshold(self, price_history, n):
        price_now = price_history[-1]
        averge_past_price = sum(price_history[-n:]) / n
        threshold = (price_now - averge_past_price) / averge_past_price
        return threshold
        
    def calculate_ema(self, current_price, n):
        if self.ema is None:
            # Initialize EMA with the first available price
            self.ema = [current_price]
        else:
            # Calculate the smoothing factor k
            k = 2 / (n + 1)
            # Calculate the new EMA value
            ema_value = (current_price * k) + (self.ema[-1] * (1 - k))

            print("     current_price: ", current_price)
            print("     k: ", k)
            print("     ema_value: ", ema_value)
            
            # Append the new EMA value to the EMA list
            self.ema.append(ema_value)

        return self.ema[-1]
        
        
    def decide(self, price_history, n):

        # Update EMA with the latest price
        current_price = price_history[-1]
        self.calculate_ema(current_price, n)

        # filtering result
        filtering_threshold = self.filtering_threshold(price_history, n)
        # ema result
        ema_threshold = (current_price - self.ema[-1]) / self.ema[-1]

        print("filtering_threshold: ", filtering_threshold)
        print("ema_threshold: ", ema_threshold)

        if self.get_open_position_subtypes() == 1:
            # rule 1 80% and rule 2 20%
            filtering_threshold = filtering_threshold * 0.8
            ema_threshold = ema_threshold * 0.2
            open_decision_value = filtering_threshold + ema_threshold
        else:
            # rule 1 20% and rule 2 80%
            filtering_threshold = filtering_threshold * 0.2
            ema_threshold = ema_threshold * 0.8
            open_decision_value = filtering_threshold + ema_threshold
        
        if self.get_close_position_subtypes() == 1:
            # rule 1 80% and rule 2 20%
            filtering_threshold = filtering_threshold * 0.8
            ema_threshold = ema_threshold * 0.2
            close_decision_value = filtering_threshold + ema_threshold
        else:
            # rule 1 20% and rule 2 80%
            filtering_threshold = filtering_threshold * 0.2
            ema_threshold = ema_threshold * 0.8
            close_decision_value = filtering_threshold + ema_threshold

        print("open_decision_value: ", open_decision_value)
        print("close_decision_value: ", close_decision_value)

        # Decide to open or close a position
        if not self.is_open_position and open_decision_value > 0:
            self.buy_btc(current_price)
            self.is_open_position = True
        elif self.is_open_position and close_decision_value < 0:
            self.sell_btc(current_price)
            self.is_open_position = False


price_history = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]

agent = chartistAgent(100, 0, 1, 1)

print(agent.get_balance())
print()

de = agent.decide(price_history, 5)

print()
print(agent.get_balance())
print(agent.get_ema())
        
    
    


