#%%
# Imports here | some to be used later
import numpy as np
import os
import json
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

#%% 
all_star_wars = {}
movies = Path('data/')
for movie in movies.iterdir():
    if 'mentions' in movie.name and 'starwars-full' not in movie.name:
        with open(movie.resolve()) as f:
            all_star_wars[movie.name] = json.load(f)
    else:
        pass
        

print(all_star_wars.keys())

# %%

all_inter_graphs = {}
for key in all_star_wars.keys():
    holistic_interaction = nx.Graph()
    if 'mentions' in key:
        all_star_wars[key] 
        for node in all_star_wars[key]['nodes']:
            holistic_interaction.add_node(node['name'])
            nx.set_node_attributes(holistic_interaction,{node['name']:node['value']}, name="Amount of Scences")

        for edge in all_star_wars[key]['links']:
            holistic_interaction.add_edge(all_star_wars[key]['nodes'][edge['source']]['name'], all_star_wars[key]['nodes'][edge['target']]['name'], weight=edge['value'] )


    all_inter_graphs[key] = holistic_interaction




# %%
# Check for proper loadings
print("Number of Nodes: {}".format(all_inter_graphs["starwars-episode-6-mentions.json"].number_of_nodes()))
print("Number of Edges: {}".format(all_inter_graphs["starwars-episode-6-mentions.json"].number_of_edges()))
print("Luke: {}".format(all_inter_graphs["starwars-episode-6-mentions.json"].nodes['LUKE']))



# %%

# Visualize the graph connections
options = {
    'node_color': 'green',
    'node_size': 100,
    'width': 1,
    'with_labels': True
}

fig = plt.figure(1, figsize=(20, 10), dpi=90)
nx.draw_kamada_kawai(all_inter_graphs["starwars-episode-6-mentions.json"], **options)

# %%
