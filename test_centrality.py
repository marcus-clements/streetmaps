import contextily as cx
import networkx as nx
import osmnx as ox
from nxempowerment.empowerment import graph_node_empowerment

ox.config(use_cache=True, log_console=True)

name = "herts_uni"
address = 'University of Hertfordshire, Hatfield, UK'
dist = 2000
n = 9
type = 'bike'

G, coords = ox.graph_from_address(
    address=address,
    dist=dist,
    # dist_type='network',
    network_type=type,
    simplify=True,
    return_coords=True
)

empvals = graph_node_empowerment(G, n)
nx.set_node_attributes(G, empvals, f'empowerment_{n}_steps')
nc = ox.plot.get_node_colors_by_attr(G, f'empowerment_{n}_steps', cmap='inferno')

fig, ax = ox.plot_graph(G, node_color=nc, edge_linewidth=1, node_size=20, figsize=(15,15))
nodes, streets = ox.graph_to_gdfs(G)
cx.add_basemap(ax=ax, source=cx.providers.Stamen.TonerLite, crs=nodes.crs, alpha=0.7)
fig.savefig(f'{name}_{type}_empowerment_{n}_step.png')
