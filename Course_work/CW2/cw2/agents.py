import numpy as np
import random

class ChartistsAgent:
    def __init__(self, market, balance_gbp, balance_btc, open_rule, close_rule):
        self.market = market
        self.balance_gbp = balance_gbp
        self.balance_btc = balance_btc
        self.open_rule = open_rule      # 1: rule 1 80% rule 2 20% 2: rule 1 20% rule 2 80%
        self.close_rule = close_rule    # 1: rule 1 80% rule 2 20% 2: rule 1 20% rule 2 80%

        self.ema_results = [market.get_current_price()]

        # positions 
        # 1: open position 2: close position
        self.positions = 2
        # # 1: buy 2: sell
        self.last_move = 0
        self.last_move_quantities = 0

    def get_open_rule(self):
        return self.open_rule
    
    def get_close_rule(self):
        return self.close_rule

    def get_positions(self):
        if self.positions == 1:
            return 'open'
        elif self.positions == 2:
            return 'close'
        
    def set_positions(self, positions):
        self.positions = positions
        
    def get_last_move(self):
        if self.last_move == 1:
            return 'buy'
        elif self.last_move == 2:
            return 'sell'

    def get_balance_gbp(self):
        return self.balance_gbp
    
    def set_balance_gbp(self, balance_gbp):
        self.balance_gbp = balance_gbp

    def add_balance_gbp(self, balance_gbp):
        self.balance_gbp += balance_gbp

    def get_balance_btc(self):
        return self.balance_btc
    
    def set_balance_btc(self, balance_btc):
        self.balance_btc = balance_btc

    def add_balance_btc(self, balance_btc):
        self.balance_btc += balance_btc
    
    def get_open_positions(self):
        return self.open_positions
    
    def set_open_positions(self, open_positions):
        self.open_positions = open_positions

    def get_wealth(self):
        wealth = self.balance_gbp + self.balance_btc * self.market.get_current_price()
        return wealth   

    def make_buy_order(self, market, price, quantity, positions, last_move, last_move_quantities):
        self.balance_gbp -= price * quantity
        market.add_order(self, 'buy', price, quantity, positions, last_move, last_move_quantities)

    def make_sell_order(self, market, price, quantity, positions, last_move, last_move_quantities):
        self.balance_btc -= quantity
        market.add_order(self, 'sell', price, quantity, positions, last_move, last_move_quantities)

    def get_filtering(self, price_history, n):
        current_price = price_history[-1]
        averge_past_price = np.mean(price_history[-n-1:-1])

        if current_price < averge_past_price:
            return 'buy'
        elif current_price > averge_past_price:
            return 'sell'
        elif current_price == averge_past_price:
            return 'hold'
        
    def get_ema(self, price_history, n):
        current_price = price_history[-1]
        # if self.ema_results is None:
        #     # Initialize EMA with the first available price
        #     self.ema_results = [current_price]

        if self.ema_results is not None:
            # Calculate the smoothing factor k
            k = 2 / (n + 1)
            # Calculate the new EMA value
            ema_value = (current_price * k) + (self.ema_results[-1] * (1 - k))
            # Append the new EMA value to the EMA list
            self.ema_results.append(ema_value)

            if current_price < ema_value:
                return 'sell'
            elif current_price > ema_value:
                return 'buy'
            elif current_price == ema_value:
                return 'hold'
            
    def decide(self, price_history, n):

        # Update EMA with the latest price
        current_price = price_history[-1]

        # filtering result
        filtering_result = self.get_filtering(price_history, n)
        # ema result
        ema_result = self.get_ema(price_history, n)

        # in open position can close position
        if self.positions == 1:
            random_number = random.random()
            if self.close_rule == 1:
                # rule 1 80% rule 2 20%
                if random_number <= 0.2:
                    result = ema_result
                else:
                    result = filtering_result
            elif self.close_rule == 2:
                # rule 1 20% rule 2 80%
                if random_number <= 0.2:
                    result = filtering_result
                else:
                    result = ema_result

            if self.last_move == 1 and result == 'sell': # last move is buy, can sell
                sell_quantity = self.last_move_quantities
                if self.balance_btc >= sell_quantity:
                    self.make_sell_order(self.market, current_price, sell_quantity, self.positions, self.last_move, self.last_move_quantities)
                    # set positions to close position
                    self.positions = 2
                    # reset last move to 0 and last move quantities to 0
                    self.last_move = 0
                    self.last_move_quantities = 0
                    
            elif self.last_move == 2 and result == 'buy': # last move is sell, can buy
                buy_quantity = self.last_move_quantities
                need_gbp = buy_quantity * current_price

                if self.balance_gbp >= need_gbp:
                    self.make_buy_order(self.market, current_price, buy_quantity, self.positions, self.last_move, self.last_move_quantities)
                    # set positions to close position
                    self.positions = 2
                    # reset last move to 0 and last move quantities to 0
                    self.last_move = 0
                    self.last_move_quantities = 0

        # in close position can open position
        elif self.positions == 2:
            random_number = random.random()
            if self.open_rule == 1:
                # rule 1 80% rule 2 20%
                if random_number <= 0.2:
                    result = ema_result
                else:
                    result = filtering_result
            elif self.open_rule == 2:
                # rule 1 20% rule 2 80%
                if random_number <= 0.2:
                    result = filtering_result
                else:
                    result = ema_result

            if result == 'buy': # last move is buy, can buy
                can_buy_quantity = self.balance_gbp / current_price
                if can_buy_quantity > 0.01:
                    buy_quantity = random.uniform(0.001, can_buy_quantity/2)
                else:
                    buy_quantity = 0

                # need_gbp = buy_quantity * current_price
                # if self.balance_gbp >= need_gbp:
                if buy_quantity > 0:
                    self.make_buy_order(self.market, current_price, buy_quantity, self.positions, self.last_move, self.last_move_quantities)
                    # set positions to open position
                    self.positions = 1
                    # set last move to buy
                    self.last_move = 1
                    # set last move quantities
                    self.last_move_quantities = buy_quantity

            if result == 'sell': # last move is sell, can sell
                can_sell_quantity = self.balance_btc
                if can_sell_quantity > 0.01:
                    sell_quantity = random.uniform(0.001, can_sell_quantity/2)
                else:
                    sell_quantity = 0

                # sell_quantity = 1
                # if self.balance_btc >= sell_quantity:
                if sell_quantity > 0:
                    self.make_sell_order(self.market, current_price, sell_quantity, self.positions, self.last_move, self.last_move_quantities)
                    # set positions to open position
                    self.positions = 1
                    # set last move to sell
                    self.last_move = 2
                    # set last move quantities
                    self.last_move_quantities = sell_quantity

class RandomAgent:
    def __init__(self, market, balance_gbp, balance_btc):
        self.market = market
        self.balance_gbp = balance_gbp
        self.balance_btc = balance_btc

        # positions 
        # 1: open position 2: close position
        self.positions = 2
        # 1: buy 2: sell
        self.last_move = 0
        self.last_move_quantities = 0

    def get_positions(self):
        if self.positions == 1:
            return 'open'
        elif self.positions == 2:
            return 'close'
        
    def get_last_move(self):
        if self.last_move == 1:
            return 'buy'
        elif self.last_move == 2:
            return 'sell'

    def get_balance_gbp(self):
        return self.balance_gbp
    
    def set_balance_gbp(self, balance_gbp):
        self.balance_gbp = balance_gbp

    def add_balance_gbp(self, balance_gbp):
        self.balance_gbp += balance_gbp

    def get_balance_btc(self):
        return self.balance_btc
    
    def set_balance_btc(self, balance_btc):
        self.balance_btc = balance_btc

    def add_balance_btc(self, balance_btc):
        self.balance_btc += balance_btc

    def get_wealth(self):
        wealth = self.balance_gbp + self.balance_btc * self.market.get_current_price()
        return wealth

    def make_buy_order(self, market, price, quantity, positions, last_move, last_move_quantities):
        self.balance_gbp -= price * quantity
        market.add_order(self, 'buy', price, quantity, positions, last_move, last_move_quantities)
        
        # self.balance_btc += quantity

    def make_sell_order(self, market, price, quantity, positions, last_move, last_move_quantities):
        self.balance_btc -= quantity
        market.add_order(self, 'sell', price, quantity, positions, last_move, last_move_quantities)
        # self.balance_gbp += price * quantity

    def decide(self, price_history, n):
        current_price = price_history[-1]

        if self.positions == 1: # open position can close position
            buy_or_sell = random.randint(1, 2)
            if buy_or_sell == 1 and self.last_move == 1: # last move is buy, can sell
                sell_quantity = self.last_move_quantities
                if self.balance_btc >= sell_quantity:
                    self.make_sell_order(self.market, current_price, sell_quantity, self.positions, self.last_move, self.last_move_quantities)
                    # set positions to close position
                    self.positions = 2
                    # set last move to sell
                    self.last_move = 0
                    self.last_move_quantities = 0

            elif buy_or_sell == 2 and self.last_move == 2: # last move is sell, can buy
                buy_quantity = self.last_move_quantities
                need_gbp = buy_quantity * current_price

                if self.balance_gbp >= need_gbp:
                    self.make_buy_order(self.market, current_price, buy_quantity, self.positions, self.last_move, self.last_move_quantities)
                    # set positions to close position
                    self.positions = 2
                    # set last move to buy
                    self.last_move = 0
                    self.last_move_quantities = 0

        elif self.positions == 2: # close position can open position
            buy_or_sell = random.randint(1, 2)
            if buy_or_sell == 1: # buy
                can_buy_quantity = self.balance_gbp / current_price
                if can_buy_quantity > 0.01:
                    buy_quantity = random.uniform(0.001, can_buy_quantity/2)
                else:
                    buy_quantity = 0

                # buy_quantity = 1
                # need_gbp = buy_quantity * current_price
                # if self.balance_gbp >= need_gbp:
                if buy_quantity > 0:
                    self.make_buy_order(self.market, current_price, buy_quantity, self.positions, self.last_move, self.last_move_quantities)
                    # set positions to open position
                    self.positions = 1
                    # set last move to buy
                    self.last_move = 1
                    self.last_move_quantities = buy_quantity

            elif buy_or_sell == 2: # sell
                can_sell_quantity = self.balance_btc
                if can_sell_quantity > 0.01:
                    sell_quantity = random.uniform(0.001, can_sell_quantity/2)
                else:
                    sell_quantity = 0


                # sell_quantity = 1
                # if self.balance_btc >= sell_quantity:
                if sell_quantity > 0:
                    self.make_sell_order(self.market, current_price, sell_quantity, self.positions, self.last_move, self.last_move_quantities)
                    # set positions to open position
                    self.positions = 1
                    # set last move to sell
                    self.last_move = 2
                    self.last_move_quantities = sell_quantity


class RSIAgent:
    def __init__(self, market, balance_gbp, balance_btc):
        self.market = market
        self.balance_gbp = balance_gbp
        self.balance_btc = balance_btc

        # positions 
        # 1: open position 2: close position
        self.positions = 2
        # 1: buy 2: sell
        self.last_move = 0
        self.last_move_quantities = 0

        self.rsi_results = []

    def get_positions(self):
        if self.positions == 1:
            return 'open'
        elif self.positions == 2:
            return 'close'
        
    def get_last_move(self):
        if self.last_move == 1:
            return 'buy'
        elif self.last_move == 2:
            return 'sell'
        
    def get_balance_gbp(self):
        return self.balance_gbp
    
    def set_balance_gbp(self, balance_gbp):
        self.balance_gbp = balance_gbp

    def add_balance_gbp(self, balance_gbp):
        self.balance_gbp += balance_gbp

    def get_balance_btc(self):
        return self.balance_btc
    
    def set_balance_btc(self, balance_btc):
        self.balance_btc = balance_btc

    def add_balance_btc(self, balance_btc):
        self.balance_btc += balance_btc

    def get_wealth(self):
        wealth = self.balance_gbp + self.balance_btc * self.market.get_current_price()
        return wealth
    
    def make_buy_order(self, market, price, quantity, positions, last_move, last_move_quantities):
        self.balance_gbp -= price * quantity
        market.add_order(self, 'buy', price, quantity, positions, last_move, last_move_quantities)
        # self.balance_btc += quantity

    def make_sell_order(self, market, price, quantity, positions, last_move, last_move_quantities):
        self.balance_btc -= quantity
        market.add_order(self, 'sell', price, quantity, positions, last_move, last_move_quantities)
        # self.balance_gbp += price * quantity
    
    def get_average_gain_loss(self, deltas, n):
        # Get the average gains and losses
        gains, losses = [], []
        for i in range(1, len(deltas)):
            if deltas[i] >= 0:
                gains.append(deltas[i])
            else:
                losses.append(abs(deltas[i]))

        avg_gain = np.mean(gains[-n:])
        avg_loss = np.mean(losses[-n:])
        return avg_gain, avg_loss
    
    def get_rsi_step(self, up, down):
        # Calculate the RSI based on average gains and losses
        rs = up / down
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def get_rsi(self, price_history, n):
        if self.rsi_results is None:
            # Initialize RSI with the first available price
            price_minus_3 = price_history[-3]
            price_minus_2 = price_history[-2]
            self.rsi_results = [price_minus_2 - price_minus_3]

        if self.rsi_results is not None:
            # Calculate the difference in price from previous step
            delta = price_history[-1] - price_history[-2]
            # Append the difference to the deltas list
            self.rsi_results.append(delta)

            # Calculate the positive gains (up) and the negative gains (down)
            up, down = self.get_average_gain_loss(self.rsi_results, n)

            # Calculate the RSI
            rsi = self.get_rsi_step(up, down)

            if rsi > 70:
                return 'sell'
            elif rsi < 30:
                return 'buy'
            elif rsi >= 30 and rsi <= 70:
                return 'hold'
            
    def decide(self, price_history, x):
        # time period n
        n = 7
        current_price = price_history[-1]

        if self.positions == 1: # open position can close position
            rsi_result = self.get_rsi(price_history, n)
            if self.last_move == 1 and rsi_result == 'sell':
                sell_quantity = self.last_move_quantities
                if self.balance_btc >= sell_quantity:
                    self.make_sell_order(self.market, current_price, sell_quantity, self.positions, self.last_move, self.last_move_quantities)
                    # set positions to close position
                    self.positions = 2
                    # set last move to sell
                    self.last_move = 0
                    self.last_move_quantities = 0

            elif self.last_move == 2 and rsi_result == 'buy':
                buy_quantity = self.last_move_quantities
                need_gbp = buy_quantity * current_price

                if self.balance_gbp >= need_gbp:
                    self.make_buy_order(self.market, current_price, buy_quantity, self.positions, self.last_move, self.last_move_quantities)
                    # set positions to close position
                    self.positions = 2
                    # set last move to buy
                    self.last_move = 0
                    self.last_move_quantities = 0

        elif self.positions == 2: # close position can open position
            rsi_result = self.get_rsi(price_history, n)
            if rsi_result == 'buy':
                can_buy_quantity = self.balance_gbp / current_price
                if can_buy_quantity > 0.01:
                    buy_quantity = random.uniform(0.001, can_buy_quantity/2)
                else:
                    buy_quantity = 0

                if buy_quantity > 0:
                    self.make_buy_order(self.market, current_price, buy_quantity, self.positions, self.last_move, self.last_move_quantities)
                    # set positions to open position
                    self.positions = 1
                    # set last move to buy
                    self.last_move = 1
                    self.last_move_quantities = buy_quantity

            elif rsi_result == 'sell':
                can_sell_quantity = self.balance_btc
                if can_sell_quantity > 0.01:
                    sell_quantity = random.uniform(0.001, can_sell_quantity/2)
                else:
                    sell_quantity = 0

                if sell_quantity > 0:
                    self.make_sell_order(self.market, current_price, sell_quantity, self.positions, self.last_move, self.last_move_quantities)
                    # set positions to open position
                    self.positions = 1
                    # set last move to sell
                    self.last_move = 2
                    self.last_move_quantities = sell_quantity


            


        

        
