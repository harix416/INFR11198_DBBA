import random
import datetime as dt
import matplotlib.pyplot as plt

from market import Market
from order_book import OrderBook, Order
from agents import ChartistsAgent, RandomAgent

random.seed(888)

def print_balance(agents):
    for agent in agents:
        b = agent.get_balance_btc()
        g = agent.get_balance_gbp()

        a = agent.get_positions()
        l = agent.get_last_move()
        print((b,g,a,l), end=" \n")


start_date = dt.date(2020, 1, 1)
end_date = dt.date(2023, 1, 31)
days = (end_date - start_date).days

price_history = [5678.0, 5623.0, 5564.5, 5549.6, 5548.8, 5595.7, 5658.4, 5532.3, 5444.2, 5422.2]

market = Market(price_history)

agent1 = ChartistsAgent(market, 10000, 100, 1, 1)
agent2 = ChartistsAgent(market, 10000, 100, 1, 2)
agent3 = ChartistsAgent(market, 10000, 100, 2, 1)
agent4 = ChartistsAgent(market, 10000, 100, 2, 2)
agent5 = ChartistsAgent(market, 10000, 100, 2, 1)
agent6 = ChartistsAgent(market, 10000, 100, 2, 2)
agent7 = ChartistsAgent(market, 10000, 100, 1, 1)
agent8 = ChartistsAgent(market, 10000, 100, 1, 2)

agent9 = RandomAgent(market, 10000, 100)
agent10 = RandomAgent(market, 10000, 100)

agents = [agent1, agent2, agent3, agent4, agent5, agent6, agent7, agent8, agent9, agent10]

# store the ratio of gbp to btc
total_gbp_btc_ratio = []
cha_gbp_btc_ratio = []
cha_11_gbp_btc_ratio = []
cha_12_gbp_btc_ratio = []
cha_21_gbp_btc_ratio = []
cha_22_gbp_btc_ratio = []
ran_gbp_btc_ratio = []
# store total wealth
total_wealth = []
cha_wealth = []
cha_11_wealth = []
cha_12_wealth = []
cha_21_wealth = []
cha_22_wealth = []
ran_wealth = []
# store number of opened positions
total_opened_positions = []
cha_opened_positions = []
cha_11_opened_positions = []
cha_12_opened_positions = []
cha_21_opened_positions = []
cha_22_opened_positions = []
ran_opened_positions = []

# store all btc in market refresh every 60 time steps
all_btc_in_market = 0

for i in range(days+1):
    print(market.get_time_step())
    print(market.get_price_history()[-1])
    print_balance(agents)

    # gbp vs btc ratio
    t_g_b_ratio = 0
    c_g_b_ratio = 0
    c_11_g_b_ratio = 0
    c_12_g_b_ratio = 0
    c_21_g_b_ratio = 0
    c_22_g_b_ratio = 0
    r_g_b_ratio = 0
    # total wealth
    t_wealth = 0
    c_wealth = 0
    c_11_wealth = 0
    c_12_wealth = 0
    c_21_wealth = 0
    c_22_wealth = 0
    r_wealth = 0
    # number of opened positions
    t_op = 0
    c_op = 0
    c_11_op = 0
    c_12_op = 0
    c_21_op = 0
    c_22_op = 0
    r_op = 0

    for agent in agents:
        agent.decide(market.get_price_history(), 8)

        btc = agent.get_balance_btc()
        gbp = agent.get_balance_gbp()
        ratio = gbp / btc
        waelth = agent.get_wealth()

        t_g_b_ratio += ratio
        t_wealth += waelth
        
        op = agent.get_positions()
        if op == 'open': t_op += 1

        if isinstance(agent, ChartistsAgent):
            c_g_b_ratio += ratio
            c_wealth += waelth
            if op == 'open': c_op += 1
            if agent.get_open_rule() == 1 and agent.get_close_rule() == 1:
                c_11_g_b_ratio += ratio
                c_11_wealth += waelth
                if op == 'open': c_11_op += 1
            elif agent.get_open_rule() == 1 and agent.get_close_rule() == 2:
                c_12_g_b_ratio += ratio
                c_12_wealth += waelth
                if op == 'open': c_12_op += 1
            elif agent.get_open_rule() == 2 and agent.get_close_rule() == 1:
                c_21_g_b_ratio += ratio
                c_21_wealth += waelth
                if op == 'open': c_21_op += 1
            elif agent.get_open_rule() == 2 and agent.get_close_rule() == 2:
                c_22_g_b_ratio += ratio
                c_22_wealth += waelth
                if op == 'open': c_22_op += 1
        elif isinstance(agent, RandomAgent):
            r_g_b_ratio += ratio
            r_wealth += waelth
            if op == 'open': r_op += 1


    total_gbp_btc_ratio.append(t_g_b_ratio)
    total_wealth.append(t_wealth)
    cha_gbp_btc_ratio.append(c_g_b_ratio)
    cha_wealth.append(c_wealth)
    cha_11_gbp_btc_ratio.append(c_11_g_b_ratio)
    cha_11_wealth.append(c_11_wealth)
    cha_12_gbp_btc_ratio.append(c_12_g_b_ratio)
    cha_12_wealth.append(c_12_wealth)
    cha_21_gbp_btc_ratio.append(c_21_g_b_ratio)
    cha_21_wealth.append(c_21_wealth)
    cha_22_gbp_btc_ratio.append(c_22_g_b_ratio)
    cha_22_wealth.append(c_22_wealth)
    ran_gbp_btc_ratio.append(r_g_b_ratio)
    ran_wealth.append(r_wealth)
    total_opened_positions.append(t_op)
    cha_opened_positions.append(c_op)
    cha_11_opened_positions.append(c_11_op)
    cha_12_opened_positions.append(c_12_op)
    cha_21_opened_positions.append(c_21_op)
    cha_22_opened_positions.append(c_22_op)
    ran_opened_positions.append(r_op)

    market.print_market_status()
    market.update_market()
    print()


    # assign btc to agents every 60 time steps
    if i%60 == 0:
        if i == 0: 
            # mark all btc
            btc_value = 0
            for agent in agents:
                b = agent.get_balance_btc()
                btc_value += b
            all_btc_in_market = btc_value
        else:
            need_to_assign = all_btc_in_market * 0.6
            # choose half of the agents randomly
            half_len_agents = len(agents) // 2
            shuffled_agents = agents.copy()
            random.shuffle(shuffled_agents)
            shuffled_agents = shuffled_agents[:half_len_agents]
            # get wealths in selected agents
            wealths = [agent.get_wealth() for agent in shuffled_agents]
            # get the btc need to assign to each agent
            all_wealth = sum(wealths)
            wealths = [w / all_wealth for w in wealths]
            wealths = [w * need_to_assign for w in wealths]
            print("wealths: ", wealths)
            # assign btc to each agent
            for i, agent in enumerate(shuffled_agents):
                agent.add_balance_btc(wealths[i])
                print("=========================")
                print(agent.get_wealth())
                print("agent ", i, " get ", wealths[i], " btc")
            all_btc_in_market = all_btc_in_market * 1.6

    
# prepare data for plotting
market_price_history = market.get_price_history()
market_price_history = market_price_history[10:]


# plt.subplot(3, 1, 1)
# plot the price history
plt.figure(1, figsize=(6, 3))
plt.plot(range(len(market_price_history)), market_price_history)
# plt.plot(range(len(market_price_history[::8])), market_price_history[::8])
plt.ticklabel_format(style='plain')  # 使用普通格式，而不是科学计数法
plt.xticks(range(0, len(market_price_history), 100))
plt.autoscale(enable=True, axis='x', tight=True)
plt.xlabel("Time step")
plt.ylabel("Price")
plt.title("Price history")

# plt.subplot(3, 1, 2)
# plot the ratio of gbp to btc
plt.figure(2, figsize=(6, 3))
plt.plot(range(len(total_gbp_btc_ratio)), total_gbp_btc_ratio)
plt.xticks(range(0, len(total_gbp_btc_ratio), 100))
plt.autoscale(enable=True, axis='x', tight=True)
plt.xlabel("Time step")
plt.ylabel("GBP/BTC ratio")
plt.title("All agents' GBP/BTC ratio")

plt.figure(3, figsize=(6, 3))
plt.plot(range(len(cha_gbp_btc_ratio)), cha_gbp_btc_ratio)
plt.xticks(range(0, len(cha_gbp_btc_ratio), 100))
plt.autoscale(enable=True, axis='x', tight=True)
plt.xlabel("Time step")
plt.ylabel("GBP/BTC ratio")
plt.title("All Chartists agents' GBP/BTC ratio")

# plt.figure(4, figsize=(6, 3))
# plt.plot(range(len(cha_11_gbp_btc_ratio)), cha_11_gbp_btc_ratio)
# plt.xticks(range(0, len(cha_11_gbp_btc_ratio), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("GBP/BTC ratio")
# plt.title("Chartists agents' 11 GBP/BTC ratio")

# plt.figure(5, figsize=(6, 3))
# plt.plot(range(len(cha_12_gbp_btc_ratio)), cha_12_gbp_btc_ratio)
# plt.xticks(range(0, len(cha_12_gbp_btc_ratio), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("GBP/BTC ratio")
# plt.title("Chartists agents' 12 GBP/BTC ratio")

# plt.figure(6, figsize=(6, 3))
# plt.plot(range(len(cha_21_gbp_btc_ratio)), cha_21_gbp_btc_ratio)
# plt.xticks(range(0, len(cha_21_gbp_btc_ratio), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("GBP/BTC ratio")
# plt.title("Chartists agents' 21 GBP/BTC ratio")

# plt.figure(7, figsize=(6, 3))
# plt.plot(range(len(cha_22_gbp_btc_ratio)), cha_22_gbp_btc_ratio)
# plt.xticks(range(0, len(cha_22_gbp_btc_ratio), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("GBP/BTC ratio")
# plt.title("Chartists agents' 22 GBP/BTC ratio")

plt.figure(8, figsize=(6, 3))
plt.plot(range(len(ran_gbp_btc_ratio)), ran_gbp_btc_ratio)
plt.xticks(range(0, len(ran_gbp_btc_ratio), 100))
plt.autoscale(enable=True, axis='x', tight=True)
plt.xlabel("Time step")
plt.ylabel("GBP/BTC ratio")
plt.title("Random agents' GBP/BTC ratio")

# plt.subplot(3, 1, 3)
# plot the total wealth
plt.figure(9, figsize=(6, 3))
plt.plot(range(len(total_wealth)), total_wealth)
plt.xticks(range(0, len(total_wealth), 100))
plt.autoscale(enable=True, axis='x', tight=True)
plt.xlabel("Time step")
plt.ylabel("Total wealth")
plt.title("All agents' total wealth")

plt.figure(10, figsize=(6, 3))
plt.plot(range(len(cha_wealth)), cha_wealth)
plt.xticks(range(0, len(cha_wealth), 100))
plt.autoscale(enable=True, axis='x', tight=True)
plt.xlabel("Time step")
plt.ylabel("Total wealth")
plt.title("All Chartists agents' total wealth")

# plt.figure(11, figsize=(6, 3))
# plt.plot(range(len(cha_11_wealth)), cha_11_wealth)
# plt.xticks(range(0, len(cha_11_wealth), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Total wealth")
# plt.title("Chartists agents' 11 total wealth")

# plt.figure(12, figsize=(6, 3))
# plt.plot(range(len(cha_12_wealth)), cha_12_wealth)
# plt.xticks(range(0, len(cha_12_wealth), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Total wealth")
# plt.title("Chartists agents' 12 total wealth")

# plt.figure(13, figsize=(6, 3))
# plt.plot(range(len(cha_21_wealth)), cha_21_wealth)
# plt.xticks(range(0, len(cha_21_wealth), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Total wealth")
# plt.title("Chartists agents' 21 total wealth")

# plt.figure(14, figsize=(6, 3))
# plt.plot(range(len(cha_22_wealth)), cha_22_wealth)
# plt.xticks(range(0, len(cha_22_wealth), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Total wealth")
# plt.title("Chartists agents' 22 total wealth")

plt.figure(15, figsize=(6, 3))
plt.plot(range(len(ran_wealth)), ran_wealth)
plt.xticks(range(0, len(ran_wealth), 100))
plt.autoscale(enable=True, axis='x', tight=True)
plt.xlabel("Time step")
plt.ylabel("Total wealth")
plt.title("Random agents' total wealth")

plt.figure(16, figsize=(6, 3))
plt.plot(range(len(total_opened_positions)), total_opened_positions)
plt.xticks(range(0, len(total_opened_positions), 100))
plt.autoscale(enable=True, axis='x', tight=True)
plt.xlabel("Time step")
plt.ylabel("Number of opened positions")
plt.title("All agents' number of opened positions")

plt.figure(17, figsize=(6, 3))
plt.plot(range(len(cha_opened_positions)), cha_opened_positions)
plt.xticks(range(0, len(cha_opened_positions), 100))
plt.autoscale(enable=True, axis='x', tight=True)
plt.xlabel("Time step")
plt.ylabel("Number of opened positions")
plt.title("All Chartists agents' number of opened positions")

# plt.figure(18, figsize=(6, 3))
# plt.plot(range(len(cha_11_opened_positions)), cha_11_opened_positions)
# plt.xticks(range(0, len(cha_11_opened_positions), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Number of opened positions")
# plt.title("Chartists agents' 11 number of opened positions")

# plt.figure(19, figsize=(6, 3))
# plt.plot(range(len(cha_12_opened_positions)), cha_12_opened_positions)
# plt.xticks(range(0, len(cha_12_opened_positions), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Number of opened positions")
# plt.title("Chartists agents' 12 number of opened positions")

# plt.figure(20, figsize=(6, 3))
# plt.plot(range(len(cha_21_opened_positions)), cha_21_opened_positions)
# plt.xticks(range(0, len(cha_21_opened_positions), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Number of opened positions")
# plt.title("Chartists agents' 21 number of opened positions")

# plt.figure(21, figsize=(6, 3))
# plt.plot(range(len(cha_22_opened_positions)), cha_22_opened_positions)
# plt.xticks(range(0, len(cha_22_opened_positions), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Number of opened positions")
# plt.title("Chartists agents' 22 number of opened positions")

plt.figure(22, figsize=(6, 3))
plt.plot(range(len(ran_opened_positions)), ran_opened_positions)
plt.xticks(range(0, len(ran_opened_positions), 100))
plt.autoscale(enable=True, axis='x', tight=True)
plt.xlabel("Time step")
plt.ylabel("Number of opened positions")
plt.title("Random agents' number of opened positions")

plt.show()





