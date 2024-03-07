import random
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

# import order_book and order classes
from order_book import OrderBook, Order


class Market:
    def __init__(self, initial_price):
        
        # self.initial_price = initial_price
        # self.start_date = start_date
        # self.end_date = end_date
        # crete other instance variables
        self.order_book = OrderBook()
        self.price_history = initial_price
        # self.total_days = (end_date - start_date).days
        self.time_step = 0  # Time step in days
    
    def get_time_step(self):
        return self.time_step
    
    # def get_total_days(self):
    #     return self.total_days
    
    # def get_current_date(self):
    #     return self.start_date + dt.timedelta(days=self.time_step)
    
    def get_price_history(self):
        return self.price_history
    
    def get_current_price(self):
        return self.price_history[-1]

    def add_order(self, agent, order_type, price, quantity, positions, last_move, last_move_quantities):
        # Add order to the market's order book.
        self.order_book.add_order(agent, order_type, price, quantity, positions, last_move, last_move_quantities)

    def update_market(self):
        
        delta_N = self.order_book.get_change_volume()

        alpha = np.sqrt(2) / 2 # Parameter limiting the minimum price shift
        price_change = alpha * np.copysign(1, delta_N) * np.sqrt(abs(np.floor(delta_N)))
        # print("~delta_N: ", delta_N)
        # print("~price_change: ", price_change)
        
        # update price history
        new_price = self.get_current_price() + price_change

        if new_price < 0:
            new_price = 0.001
        self.price_history.append(new_price)

        self.order_book.match_orders()

        # time step
        self.time_step += 1
        pass

    def print_market_status(self):
        # Print the current market status.
        current_price = self.get_current_price()
        print(f"\nCurrent Market Price: {current_price}")
        # Print the order book
        self.order_book.print_order_book()