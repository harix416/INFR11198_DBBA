import random
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

from market import Market
from agents import ChartistsAgent, RandomAgent, RSIAgent

# set random seed
random.seed(838)
# function to print balance of agents
def print_balance(agents):
    for agent in agents:
        b = agent.get_balance_btc()
        g = agent.get_balance_gbp()

        a = agent.get_positions()
        l = agent.get_last_move()
        print((b,g,a,l), end=" \n")

# set the start and end date
start_date = dt.date(2020, 1, 1)
end_date = dt.date(2023, 10, 30)

# cyberattack settings
# start_date = dt.date(2020, 1, 1)
# end_date = dt.date(2024, 3, 1)
# cyberattack_date = dt.date(2023, 12, 1)
# attack_days = (cyberattack_date - start_date).days
# print("attack days: ", attack_days)

# calculate the number of days
days = (end_date - start_date).days
# set the initial price
price_history = [5678.0, 5623.0, 5564.5, 5549.6, 5548.8, 5595.7, 5658.4, 5532.3, 5444.2, 5422.2]
market = Market(price_history)

agent1 = ChartistsAgent(market, 50000, 10, 1, 1)
agent2 = ChartistsAgent(market, 50000, 10, 1, 2)
agent3 = ChartistsAgent(market, 50000, 10, 2, 1)
agent4 = ChartistsAgent(market, 50000, 10, 2, 2)

agent5 = ChartistsAgent(market, 50000, 10, 2, 1)
agent6 = ChartistsAgent(market, 50000, 10, 2, 2)
agent7 = ChartistsAgent(market, 50000, 10, 1, 1)
agent8 = ChartistsAgent(market, 50000, 10, 1, 2)

agent9 = RandomAgent(market, 50000, 10)
agent10 = RandomAgent(market, 50000, 10)

# agent11 = RSIAgent(market, 50000, 10)
# agent12 = RSIAgent(market, 50000, 10)

agents = [agent1, agent2, agent3, agent4, agent5, agent6, agent7, agent8,agent9, agent10]
# agents = [agent1, agent2, agent3, agent4, agent5, agent6, agent7, agent8,agent9, agent10, agent11, agent12]

# store the ratio of gbp to btc
total_gbp_btc_ratio = []
cha_gbp_btc_ratio = []
cha_11_gbp_btc_ratio = []
cha_12_gbp_btc_ratio = []
cha_21_gbp_btc_ratio = []
cha_22_gbp_btc_ratio = []
ran_gbp_btc_ratio = []
rsi_gbp_btc_ratio = []
# store total wealth of agents
total_wealth = []
cha_wealth = []
cha_11_wealth = []
cha_12_wealth = []
cha_21_wealth = []
cha_22_wealth = []
ran_wealth = []
rsi_wealth = []
# store gbp of agents
total_gbp = []
cha_gbp = []
cha_11_gbp = []
cha_12_gbp = []
cha_21_gbp = []
cha_22_gbp = []
ran_gbp = []
rsi_gbp = []
# store btc of agents
total_btc = []
cha_btc = []
cha_11_btc = []
cha_12_btc = []
cha_21_btc = []
cha_22_btc = []
ran_btc = []
rsi_btc = []
# store number of opened positions  of agents
total_opened_positions = []
cha_opened_positions = []
cha_11_opened_positions = []
cha_12_opened_positions = []
cha_21_opened_positions = []
cha_22_opened_positions = []
ran_opened_positions = []
rsi_opened_positions = []

# store all btc in market use for refresh every 60 time steps
all_btc_in_market = 0
attacked_agents = random.sample(agents, int(0.4 * len(agents)))

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
    s_g_b_ratio = 0
    # total wealth
    t_wealth = 0
    c_wealth = 0
    c_11_wealth = 0
    c_12_wealth = 0
    c_21_wealth = 0
    c_22_wealth = 0
    r_wealth = 0
    s_wealth = 0
    # gbp
    t_gbp = 0
    c_gbp = 0
    c_11_gbp = 0
    c_12_gbp = 0
    c_21_gbp = 0
    c_22_gbp = 0
    r_gbp = 0
    s_gbp = 0
    # btc
    t_btc = 0
    c_btc = 0
    c_11_btc = 0
    c_12_btc = 0
    c_21_btc = 0
    c_22_btc = 0
    r_btc = 0
    s_btc = 0
    # number of opened positions
    t_op = 0
    c_op = 0
    c_11_op = 0
    c_12_op = 0
    c_21_op = 0
    c_22_op = 0
    r_op = 0
    s_op = 0

    for agent in agents:

        # use for cyberattack
        # if i == attack_days:
        #     if agent in attacked_agents:
        #         print("agent ", agent, " is attacked")
        #         btc_quan = agent.get_balance_btc()
        #         if btc_quan > 0:
        #             agent.make_sell_order(market, market.get_current_price(), btc_quan, 3, 1, btc_quan)
        #             agent.positions = 3
        #             agent.last_move = 1
        #             agent.last_move_quantities = btc_quan

        # agent decide 
        agent.decide(market.get_price_history(), 5)
        
        btc = agent.get_balance_btc()
        gbp = agent.get_balance_gbp()
        if btc == 0:
            ratio = 0
        else:
            ratio = gbp / btc
        waelth = agent.get_wealth()

        # collect data
        t_g_b_ratio += ratio
        t_wealth += waelth
        t_gbp += gbp
        t_btc += btc
        
        op = agent.get_positions()
        if op == 'open': t_op += 1

        if isinstance(agent, ChartistsAgent):
            c_g_b_ratio += ratio
            c_wealth += waelth
            c_gbp += gbp
            c_btc += btc
            if op == 'open': c_op += 1
            if agent.get_open_rule() == 1 and agent.get_close_rule() == 1:
                c_11_g_b_ratio += ratio
                c_11_wealth += waelth
                c_11_btc += btc
                c_11_gbp += gbp
                if op == 'open': c_11_op += 1
            elif agent.get_open_rule() == 1 and agent.get_close_rule() == 2:
                c_12_g_b_ratio += ratio
                c_12_wealth += waelth
                c_12_gbp += gbp
                c_12_btc += btc
                if op == 'open': c_12_op += 1
            elif agent.get_open_rule() == 2 and agent.get_close_rule() == 1:
                c_21_g_b_ratio += ratio
                c_21_wealth += waelth
                c_21_gbp += gbp
                c_21_btc += btc
                if op == 'open': c_21_op += 1
            elif agent.get_open_rule() == 2 and agent.get_close_rule() == 2:
                c_22_g_b_ratio += ratio
                c_22_wealth += waelth
                c_22_gbp += gbp
                c_22_btc += btc
                if op == 'open': c_22_op += 1
        elif isinstance(agent, RandomAgent):
            r_g_b_ratio += ratio
            r_wealth += waelth
            r_gbp += gbp
            r_btc += btc
            if op == 'open': r_op += 1
        elif isinstance(agent, RSIAgent):
            s_g_b_ratio += ratio
            s_wealth += waelth
            s_gbp += gbp
            s_btc += btc
            if op == 'open': s_op += 1


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
    rsi_gbp_btc_ratio.append(s_g_b_ratio)
    rsi_wealth.append(s_wealth)
    total_opened_positions.append(t_op)
    cha_opened_positions.append(c_op)
    cha_11_opened_positions.append(c_11_op)
    cha_12_opened_positions.append(c_12_op)
    cha_21_opened_positions.append(c_21_op)
    cha_22_opened_positions.append(c_22_op)
    ran_opened_positions.append(r_op)
    rsi_opened_positions.append(s_op)
    total_gbp.append(t_gbp)
    total_btc.append(t_btc)
    cha_gbp.append(c_gbp)
    cha_btc.append(c_btc)
    cha_11_gbp.append(c_11_gbp)
    cha_11_btc.append(c_11_btc)
    cha_12_gbp.append(c_12_gbp)
    cha_12_btc.append(c_12_btc)
    cha_21_gbp.append(c_21_gbp)
    cha_21_btc.append(c_21_btc)
    cha_22_gbp.append(c_22_gbp)
    cha_22_btc.append(c_22_btc)
    ran_gbp.append(r_gbp)
    ran_btc.append(r_btc)
    rsi_gbp.append(s_gbp)
    rsi_btc.append(s_btc)
    

    # print the market status
    market.print_market_status()
    # update the market
    market.update_market()
    print()

    # remove attacked agents
    a_list = []
    for agent in agents:
        if agent not in attacked_agents:
            a_list.append(agent)

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
            half_len_agents = len(a_list) // 2
            shuffled_agents = a_list.copy()
            random.shuffle(shuffled_agents)
            shuffled_agents = shuffled_agents[:half_len_agents]
            # get wealths in selected agents
            wealths = [agent.get_wealth() for agent in shuffled_agents]
            # get the btc need to assign to each agent
            all_wealth = sum(wealths)
            wealths = [w / all_wealth for w in wealths]
            wealths = [w * need_to_assign for w in wealths]
            # assign btc to each agent
            for i, agent in enumerate(shuffled_agents):
                agent.add_balance_btc(wealths[i])
            all_btc_in_market = all_btc_in_market * 1.6

    
# prepare data for plotting
market_price_history = market.get_price_history()
market_price_history = market_price_history[10:] # remove the first 10 days

# plot the price history
plt.figure(1, figsize=(10, 5))
plt.plot(range(len(market_price_history)), market_price_history)
plt.ticklabel_format(style='plain')
plt.xticks(range(0, len(market_price_history), 100))
plt.autoscale(enable=True, axis='x', tight=True)
plt.xlabel("Time step")
plt.ylabel("Price")
plt.title("Price history")

plt.show()

# plt.figure(2, figsize=(10, 5))
# # plt.plot(range(len(total_gbp_btc_ratio)), total_gbp_btc_ratio, label='All agents')
# # plt.plot(range(len(cha_gbp_btc_ratio)), cha_gbp_btc_ratio, label='Chartists agents')
# plt.plot(range(len(cha_11_gbp_btc_ratio)), cha_11_gbp_btc_ratio, label='Chartists agents 11', color='red')
# plt.plot(range(len(cha_12_gbp_btc_ratio)), cha_12_gbp_btc_ratio, label='Chartists agents 12', color='orange')
# plt.xticks(range(0, len(total_gbp_btc_ratio), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("GBP/BTC ratio")
# plt.legend()
# plt.title("Chartists agents' GBP/BTC ratio")

# plt.figure(3, figsize=(10, 5))
# plt.plot(range(len(cha_21_gbp_btc_ratio)), cha_21_gbp_btc_ratio, label='Chartists agents 21', color='green')
# plt.plot(range(len(cha_22_gbp_btc_ratio)), cha_22_gbp_btc_ratio, label='Chartists agents 22', color='blue')
# plt.xticks(range(0, len(total_gbp_btc_ratio), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("GBP/BTC ratio")
# plt.legend()
# plt.title("Chartists agents' GBP/BTC ratio")

# plt.figure(4, figsize=(10, 5))
# plt.plot(range(len(ran_gbp_btc_ratio)), ran_gbp_btc_ratio, label='Random agents', color='purple')
# plt.xticks(range(0, len(total_gbp_btc_ratio), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("GBP/BTC ratio")
# plt.legend()
# plt.title("Random agents' GBP/BTC ratio")

# plt.figure(5, figsize=(10, 10))
# # plt.plot(range(len(cha_wealth)), cha_wealth, label='Chartists agents')
# plt.plot(range(len(cha_11_wealth)), cha_11_wealth, label='Chartists agents 11')
# plt.plot(range(len(cha_12_wealth)), cha_12_wealth, label='Chartists agents 12')
# plt.plot(range(len(cha_21_wealth)), cha_21_wealth, label='Chartists agents 21')
# plt.plot(range(len(cha_22_wealth)), cha_22_wealth, label='Chartists agents 22')
# plt.plot(range(len(ran_wealth)), ran_wealth, label='Random agents')
# plt.xticks(range(0, len(cha_wealth), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Total wealth")
# plt.legend()
# plt.title("All agents' total wealth")

# plt.figure(6, figsize=(10, 10))
# plt.plot(range(len(ran_wealth)), ran_wealth, label='Random agents')
# plt.xticks(range(0, len(cha_wealth), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Total wealth")
# plt.legend()
# plt.title("Random agents' total wealth")

# plt.figure(7, figsize=(10, 10))
# plt.plot(range(len(rsi_wealth)), rsi_wealth, label='RSI agents')
# plt.xticks(range(0, len(rsi_wealth), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Total wealth")
# plt.legend()
# plt.title("RSI agents' total wealth")


# plt.figure(8, figsize=(10, 10))
# # plt.plot(range(len(total_btc)), total_btc)
# # plt.plot(range(len(cha_btc)), cha_btc)
# plt.plot(range(len(cha_11_btc)), cha_11_btc, label='Chartists agents 11')
# plt.plot(range(len(cha_12_btc)), cha_12_btc, label='Chartists agents 12')
# plt.plot(range(len(cha_21_btc)), cha_21_btc, label='Chartists agents 21')
# plt.plot(range(len(cha_22_btc)), cha_22_btc, label='Chartists agents 22')
# plt.plot(range(len(ran_btc)), ran_btc, label='Random agents')
# plt.xticks(range(0, len(total_btc), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("BTC")
# plt.legend()
# plt.title("Agents' BTC")

# plt.figure(9, figsize=(10, 10))
# plt.plot(range(len(ran_btc)), ran_btc, label='Random agents')
# plt.xticks(range(0, len(total_btc), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("BTC")
# plt.legend()
# plt.title("Random agents' BTC")

# plt.figure(10, figsize=(10, 10))
# # plt.plot(range(len(total_gbp)), total_gbp)
# # plt.plot(range(len(cha_gbp)), cha_gbp)
# plt.plot(range(len(cha_11_gbp)), cha_11_gbp, label='Chartists agents 11')
# plt.plot(range(len(cha_12_gbp)), cha_12_gbp, label='Chartists agents 12')
# plt.plot(range(len(cha_21_gbp)), cha_21_gbp, label='Chartists agents 21')
# plt.plot(range(len(cha_22_gbp)), cha_22_gbp, label='Chartists agents 22')
# plt.plot(range(len(ran_gbp)), ran_gbp, label='Random agents')
# plt.xticks(range(0, len(total_gbp), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("GBP")
# plt.legend()
# plt.title("Agents' GBP")

# plt.figure(11, figsize=(10, 10))
# plt.plot(range(len(ran_gbp)), ran_gbp, label='Random agents')
# plt.xticks(range(0, len(total_gbp), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("GBP")
# plt.legend()
# plt.title("Random agents' GBP")

# collect data of number of opened positions
# print("opened positions: ", sum(total_opened_positions))
# print("cha opened positions: ", sum(cha_opened_positions))
# print("cha 11 opened positions: ", sum(cha_11_opened_positions))
# print("cha 12 opened positions: ", sum(cha_12_opened_positions))
# print("cha 21 opened positions: ", sum(cha_21_opened_positions))
# print("cha 22 opened positions: ", sum(cha_22_opened_positions))
# print("ran opened positions: ", sum(ran_opened_positions))

# plt.show()




