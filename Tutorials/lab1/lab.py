import networkx as nx
import pandas as pd

# Read in the data
df = pd.read_csv('retadjusted.csv')
df = df.rename(columns=lambda x: x.replace('ret.adjusted.prices.', ''))

# Create a correlation matrix
numeric_cols = df.select_dtypes(include='number').columns
corr_matrix = df[numeric_cols].corr(method='pearson')

# Create a graph from the correlation matrix
G = nx.from_pandas_adjacency(corr_matrix)

# Draw the graph
nx.draw(G, with_labels=True)

def max_degree_num(G,i):
    tps = []
    tp = ()
    for node in G.nodes():
        tp = (node,G.degree(node))
        tps.append(tp)
    sorted_tps = sorted(tps, key=lambda x: x[1], reverse=True)
    return sorted_tps[:i]