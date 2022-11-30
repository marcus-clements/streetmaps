import logging

import networkx as nx
import osmnx as ox
import pandas as pd
import seaborn as sns
import numpy as np

import matplotlib.pyplot as plt

from nxempowerment.empowerment import graph_node_empowerment

logger = logging.getLogger(__name__)

ox.config(use_cache=True, log_console=True)
print(ox.__version__)

# G = ox.graph_from_address('76 Queen\'s Park Rise, Brighton, BN2 9ZF, UK', network_type='walk')
G = ox.graph_from_address('76 Queen\'s Park Rise, Brighton, BN2 9ZF, UK', network_type='walk')
# fig, ax = ox.plot_graph(G)
# fig.savefig('test.png')

# edge_centrality = nx.closeness_centrality(nx.line_graph(G))
# nx.set_edge_attributes(G, edge_centrality, 'edge_centrality')
# ec = ox.plot.get_edge_colors_by_attr(G, 'edge_centrality', cmap='inferno')
# fig, ax = ox.plot_graph(G, edge_color=ec, edge_linewidth=2, node_size=10)
# fig.savefig('qp_edge_centrality.png')

for n in range(1, 10):
    empvals = graph_node_empowerment(G, n)
    nx.set_node_attributes(G, empvals, f'empowerment_{n}')
    # nc = ox.plot.get_node_colors_by_attr(G, f'empowerment_{n}_step', cmap='inferno')
    # fig, ax = ox.plot_graph(G, node_color=nc, edge_linewidth=1, node_size=20)
    # fig.savefig(f'qp_empowerment_{n}_step.png')

for n in range(1, 10):
    nx.set_node_attributes(G, nx.load_centrality(G, cutoff=n), f'load_centrality_{n}')

nx.set_node_attributes(G, nx.harmonic_centrality(G), 'harmonic_centrality')

voterank = nx.voterank(G)
node_voterank = {n: k for k, n in enumerate(voterank)}
nx.set_node_attributes(G, node_voterank, 'voterank')

df = pd.DataFrame.from_dict(dict(G.nodes(data=True)), orient='index')

corr = df.corr()

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
f.savefig('heatmap.png')
