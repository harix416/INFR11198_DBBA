from agents import ChartistsAgent

class Order:
    def __init__(self, agent, order_type, price, quantity, positions, last_move, last_move_quantities):
        self.agent = agent
        self.order_type = order_type
        self.price = price
        self.quantity = quantity
        self.positions = positions
        self.last_move = last_move
        self.last_move_quantities = last_move_quantities


    def get_agent(self):
        return self.agent

    def get_order_type(self):
        return self.order_type
    
    def set_order_type(self, order_type):
        self.order_type = order_type
    
    def get_price(self):
        return self.price
    
    def set_price(self, price):
        self.price = price
    
    def get_quantity(self):
        return self.quantity
    
    def set_quantity(self, quantity):
        self.quantity = quantity

    def get_positions(self):
        return self.positions
    
    def set_positions(self, positions):
        self.positions = positions

    def get_last_move(self):
        return self.last_move
    
    def set_last_move(self, last_move):
        self.last_move = last_move

    def get_last_move_quantities(self):
        return self.last_move_quantities
    
    def set_last_move_quantities(self, last_move_quantities):
        self.last_move_quantities = last_move_quantities

class OrderBook:
    def __init__(self):
        self.buy_orders = []  # List of buy orders, each order is a tuple (price, quantity)
        self.sell_orders = []  # List of sell orders, each order is a tuple (price, quantity)

    def clear_order_book(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, agent, order_type, price, quantity, positions, last_move, last_move_quantities):
        # set order
        order = Order(agent, order_type, price, quantity, positions, last_move, last_move_quantities)

        if order_type == 'buy':
            self.buy_orders.append(order)
        elif order_type == 'sell': # sell order
            self.sell_orders.append(order)

        self.sort_orders()

    def sort_orders(self):
        self.buy_orders.sort(key=lambda x: x.quantity, reverse=True)
        self.sell_orders.sort(key=lambda x: x.quantity, reverse=True)

    def remove_order(self, order):
        if order.get_order_type() == 'buy':
            self.buy_orders.remove(order)
        elif order.get_order_type() == 'sell':
            self.sell_orders.remove(order)        

    def get_top_order(self, buy_or_sell):
        if buy_or_sell == 'buy':
            return self.buy_orders[0]
        elif buy_or_sell == 'sell':
            return self.sell_orders[0]

    def match_orders(self):
        while self.buy_orders:
            # Get top buy orders
            top_buy_order = self.get_top_order('buy')
            top_buy_price = top_buy_order.get_price()
            top_buy_quantity = top_buy_order.get_quantity()

            top_buy_order_agent = top_buy_order.get_agent()
            top_buy_order_agent.set_balance_btc(top_buy_order_agent.get_balance_btc() + top_buy_quantity)

            self.remove_order(top_buy_order)

        while self.sell_orders:
            # Get top sell orders
            top_sell_order = self.get_top_order('sell')
            top_sell_price = top_sell_order.get_price()
            top_sell_quantity = top_sell_order.get_quantity()

            top_sell_order_agent = top_sell_order.get_agent()
            top_sell_order_agent.set_balance_gbp(top_sell_order_agent.get_balance_gbp() + top_sell_price * top_sell_quantity)

            self.remove_order(top_sell_order)

        # while self.buy_orders and self.sell_orders:
            
        #     # Get top buy and sell orders
        #     top_buy_order = self.get_top_order('buy')
        #     top_sell_order = self.get_top_order('sell')
        #     top_buy_price = top_buy_order.get_price()
        #     top_sell_price = top_sell_order.get_price()
        #     top_buy_quantity = top_buy_order.get_quantity()
        #     top_sell_quantity = top_sell_order.get_quantity()

        #     # Price of top buy order >= price of top sell order 
        #     if top_buy_price >= top_sell_price: 
        #         # Update quantities or remove orders if quantity becomes zero
        #         print(f"Matched order for buy quantity {top_buy_quantity} at price {top_buy_price} and sell quantity {top_sell_quantity} at price {top_sell_price}")

        #         # Buy order quantity > sell order quantity
        #         if top_buy_quantity == top_sell_quantity:
        #             # remove both orders
        #             self.remove_order(top_buy_order)
        #             self.remove_order(top_sell_order)
        #             top_buy_order_agent = top_buy_order.get_agent()
        #             top_sell_order_agent = top_sell_order.get_agent()
        #             top_buy_order_agent.set_balance_btc(top_buy_order_agent.get_balance_btc() + top_buy_quantity)
        #             top_sell_order_agent.set_balance_gbp(top_sell_order_agent.get_balance_gbp() + top_sell_price * top_sell_quantity)
        #         elif top_buy_quantity > top_sell_quantity:
        #             # Remove sell order
        #             self.remove_order(top_sell_order)
        #             # set buy order quantity = buy order quantity - sell order quantity
        #             top_buy_order.set_quantity(top_buy_quantity - top_sell_quantity)

        #             top_buy_order_agent = top_buy_order.get_agent()
        #             top_sell_order_agent = top_sell_order.get_agent()
        #             top_buy_order_agent.set_balance_btc(top_buy_order_agent.get_balance_btc() + top_sell_quantity)
        #             top_sell_order_agent.set_balance_gbp(top_sell_order_agent.get_balance_gbp() + top_sell_price * top_sell_quantity)
        #         elif top_buy_quantity < top_sell_quantity:
        #             # Remove buy order
        #             self.remove_order(top_buy_order)
        #             # set sell order quantity = sell order quantity - buy order quantity
        #             top_sell_order.set_quantity(top_sell_quantity - top_buy_quantity)

        #             top_buy_order_agent = top_buy_order.get_agent()
        #             top_sell_order_agent = top_sell_order.get_agent()
        #             top_buy_order_agent.set_balance_btc(top_buy_order_agent.get_balance_btc() + top_buy_quantity)
        #             top_sell_order_agent.set_balance_gbp(top_sell_order_agent.get_balance_gbp() + top_sell_price * top_buy_quantity)
        
        # if self.buy_orders or self.sell_orders:

        #     # return order and reset factor if no orders match
        #     for order in self.buy_orders:
        #         agent = order.get_agent()
        #         agent.set_balance_gbp(agent.get_balance_gbp() + order.get_price() * order.get_quantity())
        #         # set positions and last move
        #         agent.positions = order.get_positions()
        #         agent.last_move = order.get_last_move()
        #         last_move_quantities = order.get_last_move_quantities()
        #         if last_move_quantities == 0:
        #             agent.last_move_quantities = 0
        #         else:
        #             agent.last_move_quantities = order.get_quantity()
        #     for order in self.sell_orders:
        #         agent = order.get_agent()
        #         agent.set_balance_btc(agent.get_balance_btc() + order.get_quantity())
        #         # set positions and last move
        #         agent.positions = order.get_positions()
        #         agent.last_move = order.get_last_move()
        #         last_move_quantities = order.get_last_move_quantities()
        #         if last_move_quantities == 0:
        #             agent.last_move_quantities = 0
        #         else:
        #             agent.last_move_quantities = order.get_quantity()

        #     self.clear_order_book()

    def get_change_volume(self):
        change_volume = 0
        for order in self.buy_orders:
            buy_order_price = order.get_price()
            buy_order_quantity = order.get_quantity()
            # change_volume += buy_order_price * buy_order_quantity
            change_volume +=buy_order_quantity

        for order in self.sell_orders:
            sell_order_price = order.get_price()
            sell_order_quantity = order.get_quantity()
            # change_volume -= sell_order_price * sell_order_quantity
            change_volume -= sell_order_quantity
        return change_volume
    
    def print_order_book(self):
        print("\tBuy Orders:")
        for order in self.buy_orders:
            top_buy_price = order.get_price()
            top_buy_quantity = order.get_quantity()
            print(f"\t\tPrice: {top_buy_price}, Quantity: {top_buy_quantity}")
        print("\tSell Orders:")
        for order in self.sell_orders:
            top_sell_price = order.get_price()
            top_sell_quantity = order.get_quantity()
            print(f"\t\tPrice: {top_sell_price}, Quantity: {top_sell_quantity}")
