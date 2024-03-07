import random
import datetime as dt
import matplotlib.pyplot as plt

from market import Market
from agents import ChartistsAgent, RandomAgent, RSIAgent

random.seed(838) # for task 2 best
# random.seed(800) # for task 5

def print_balance(agents):
    for agent in agents:
        b = agent.get_balance_btc()
        g = agent.get_balance_gbp()

        a = agent.get_positions()
        l = agent.get_last_move()
        print((b,g,a,l), end=" \n")


start_date = dt.date(2020, 1, 1)
end_date = dt.date(2023, 10, 30)

# cyberattack
# start_date = dt.date(2020, 1, 1)
# end_date = dt.date(2024, 3, 1)
# cyberattack_date = dt.date(2023, 12, 1)
# attack_days = (cyberattack_date - start_date).days

days = (end_date - start_date).days

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

agent11 = RSIAgent(market, 50000, 10)
agent12 = RSIAgent(market, 50000, 10)


agents = [agent1, agent2, agent3, agent4, agent5, agent6, agent7, agent8,agent9, agent10]
# agents = [agent1, agent2, agent3, agent4, agent5, agent6, agent7, agent8,agent9, agent10, agent11, agent12]

tw=[]
cw=[]
rw=[]

for kkk in range(10,200,10):
    # store total wealth
    total_wealth = []
    cha_wealth = []
    ran_wealth = []

    # store all btc in market refresh every 60 time steps
    all_btc_in_market = 0
    attacked_agents = random.sample(agents, int(0.4 * len(agents)))

    for i in range(days+1):
        print(market.get_time_step())
        print(market.get_price_history()[-1])
        print_balance(agents)

        # total wealth
        t_wealth = 0
        c_wealth = 0
        r_wealth = 0

        for agent in agents:

                    
            agent.decide(market.get_price_history(), kkk)
            waelth = agent.get_wealth()
            t_wealth += waelth

            if isinstance(agent, ChartistsAgent):
                c_wealth += waelth
            elif isinstance(agent, RandomAgent):
                r_wealth += waelth

        total_wealth.append(t_wealth)
        cha_wealth.append(c_wealth)
        ran_wealth.append(r_wealth)

        market.print_market_status()
        market.update_market()
        print()

        
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
                # print("wealths: ", wealths)
                # assign btc to each agent
                for i, agent in enumerate(shuffled_agents):
                    agent.add_balance_btc(wealths[i])
                all_btc_in_market = all_btc_in_market * 1.6
    
    tw.append(total_wealth[-1])
    cw.append(cha_wealth[-1])
    rw.append(ran_wealth[-1])


plt.figure(1, figsize=(10, 5))
plt.plot(range(len(tw)), tw)
plt.xticks(range(0, len(tw), 1))
plt.autoscale(enable=True, axis='x', tight=True)
plt.xlabel("n value")
plt.ylabel("Total wealth")

plt.figure(2, figsize=(10, 5))
plt.plot(range(len(cw)), cw)
plt.xticks(range(0, len(cw), 1))
plt.autoscale(enable=True, axis='x', tight=True)
plt.xlabel("n value")
plt.ylabel("Cha Agents' Total wealth")

plt.figure(3, figsize=(10, 5))
plt.plot(range(len(rw)), rw)
plt.xticks(range(0, len(rw), 1))
plt.autoscale(enable=True, axis='x', tight=True)
plt.xlabel("n value")
plt.ylabel("Random Traders' Total wealth")




# # prepare data for plotting
# market_price_history = market.get_price_history()
# market_price_history = market_price_history[10:]


# # plot the price history
# plt.figure(1, figsize=(10, 5))
# plt.plot(range(len(market_price_history)), market_price_history)
# # plt.plot(range(len(market_price_history[::8])), market_price_history[::8])
# plt.ticklabel_format(style='plain')  # 使用普通格式，而不是科学计数法
# plt.xticks(range(0, len(market_price_history), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Price")
# plt.title("Price history")

# # plt.subplot(3, 1, 2)
# # plot the ratio of gbp to btc
# plt.figure(2, figsize=(10, 5))
# plt.plot(range(len(total_gbp_btc_ratio)), total_gbp_btc_ratio)
# plt.xticks(range(0, len(total_gbp_btc_ratio), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("GBP/BTC ratio")
# plt.title("All agents' GBP/BTC ratio")

# plt.figure(3, figsize=(10, 5))
# plt.plot(range(len(cha_gbp_btc_ratio)), cha_gbp_btc_ratio)
# plt.xticks(range(0, len(cha_gbp_btc_ratio), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("GBP/BTC ratio")
# plt.title("All Chartists agents' GBP/BTC ratio")

# plt.figure(4, figsize=(10, 5))
# plt.plot(range(len(cha_11_gbp_btc_ratio)), cha_11_gbp_btc_ratio)
# plt.xticks(range(0, len(cha_11_gbp_btc_ratio), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("GBP/BTC ratio")
# plt.title("Chartists agents' 11 GBP/BTC ratio")

# plt.figure(5, figsize=(10, 5))
# plt.plot(range(len(cha_12_gbp_btc_ratio)), cha_12_gbp_btc_ratio)
# plt.xticks(range(0, len(cha_12_gbp_btc_ratio), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("GBP/BTC ratio")
# plt.title("Chartists agents' 12 GBP/BTC ratio")

# plt.figure(6, figsize=(10, 5))
# plt.plot(range(len(cha_21_gbp_btc_ratio)), cha_21_gbp_btc_ratio)
# plt.xticks(range(0, len(cha_21_gbp_btc_ratio), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("GBP/BTC ratio")
# plt.title("Chartists agents' 21 GBP/BTC ratio")

# plt.figure(7, figsize=(10, 5))
# plt.plot(range(len(cha_22_gbp_btc_ratio)), cha_22_gbp_btc_ratio)
# plt.xticks(range(0, len(cha_22_gbp_btc_ratio), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("GBP/BTC ratio")
# plt.title("Chartists agents' 22 GBP/BTC ratio")

# plt.figure(8, figsize=(10, 5))
# plt.plot(range(len(ran_gbp_btc_ratio)), ran_gbp_btc_ratio)
# plt.xticks(range(0, len(ran_gbp_btc_ratio), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("GBP/BTC ratio")
# plt.title("Random agents' GBP/BTC ratio")

# plt.figure(9, figsize=(10, 5))
# plt.plot(range(len(total_wealth)), total_wealth)
# plt.xticks(range(0, len(total_wealth), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Total wealth")
# plt.title("All agents' total wealth")

# plt.figure(10, figsize=(10, 5))
# plt.plot(range(len(cha_wealth)), cha_wealth)
# plt.xticks(range(0, len(cha_wealth), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Total wealth")
# plt.title("All Chartists agents' total wealth")

# plt.figure(11, figsize=(10, 5))
# plt.plot(range(len(cha_11_wealth)), cha_11_wealth)
# plt.xticks(range(0, len(cha_11_wealth), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Total wealth")
# plt.title("Chartists agents' 11 total wealth")

# plt.figure(12, figsize=(10, 5))
# plt.plot(range(len(cha_12_wealth)), cha_12_wealth)
# plt.xticks(range(0, len(cha_12_wealth), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Total wealth")
# plt.title("Chartists agents' 12 total wealth")

# plt.figure(13, figsize=(10, 5))
# plt.plot(range(len(cha_21_wealth)), cha_21_wealth)
# plt.xticks(range(0, len(cha_21_wealth), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Total wealth")
# plt.title("Chartists agents' 21 total wealth")

# plt.figure(14, figsize=(10, 5))
# plt.plot(range(len(cha_22_wealth)), cha_22_wealth)
# plt.xticks(range(0, len(cha_22_wealth), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Total wealth")
# plt.title("Chartists agents' 22 total wealth")

# plt.figure(15, figsize=(10, 5))
# plt.plot(range(len(ran_wealth)), ran_wealth)
# plt.xticks(range(0, len(ran_wealth), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Total wealth")
# plt.title("Random agents' total wealth")

# plt.figure(16, figsize=(10, 5))
# plt.plot(range(len(rsi_wealth)), rsi_wealth)
# plt.xticks(range(0, len(rsi_wealth), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Total wealth")
# plt.title("RSI agents' total wealth")

# plt.figure(17, figsize=(10, 5))
# plt.plot(range(len(total_opened_positions)), total_opened_positions)
# plt.xticks(range(0, len(total_opened_positions), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Number of opened positions")
# plt.title("All agents' number of opened positions")

# plt.figure(18, figsize=(10, 5))
# plt.plot(range(len(cha_opened_positions)), cha_opened_positions)
# plt.xticks(range(0, len(cha_opened_positions), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Number of opened positions")
# plt.title("All Chartists agents' number of opened positions")

# plt.figure(19, figsize=(10, 5))
# plt.plot(range(len(cha_11_opened_positions)), cha_11_opened_positions)
# plt.xticks(range(0, len(cha_11_opened_positions), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Number of opened positions")
# plt.title("Chartists agents' 11 number of opened positions")

# plt.figure(20, figsize=(10, 5))
# plt.plot(range(len(cha_12_opened_positions)), cha_12_opened_positions)
# plt.xticks(range(0, len(cha_12_opened_positions), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Number of opened positions")
# plt.title("Chartists agents' 12 number of opened positions")

# plt.figure(21, figsize=(10, 5))
# plt.plot(range(len(cha_21_opened_positions)), cha_21_opened_positions)
# plt.xticks(range(0, len(cha_21_opened_positions), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Number of opened positions")
# plt.title("Chartists agents' 21 number of opened positions")

# plt.figure(22, figsize=(10, 5))
# plt.plot(range(len(cha_22_opened_positions)), cha_22_opened_positions)
# plt.xticks(range(0, len(cha_22_opened_positions), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Number of opened positions")
# plt.title("Chartists agents' 22 number of opened positions")

# plt.figure(23, figsize=(10, 5))
# plt.plot(range(len(ran_opened_positions)), ran_opened_positions)
# plt.xticks(range(0, len(ran_opened_positions), 100))
# plt.autoscale(enable=True, axis='x', tight=True)
# plt.xlabel("Time step")
# plt.ylabel("Number of opened positions")
# plt.title("Random agents' number of opened positions")



plt.show()





