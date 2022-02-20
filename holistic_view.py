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
    if 'interactions-allCharacters' in movie.name and 'starwars-full' not in movie.name:
        with open(movie.resolve()) as f:
            all_star_wars[movie.name] = json.load(f)
    else:
        pass
        

print(all_star_wars.keys())

# %%

all_inter_graphs = {}
for key in all_star_wars.keys():
    holistic_interaction = nx.Graph()
    if 'interactions' in key:
        all_star_wars[key] 
        for node in all_star_wars[key]['nodes']:
            holistic_interaction.add_node(node['name'])
        
        for edge in all_star_wars[key]['links']:
            holistic_interaction.add_edge(all_star_wars[key]['nodes'][edge['source']]['name'], all_star_wars[key]['nodes'][edge['target']]['name'])


    all_inter_graphs[key] = holistic_interaction




# %%
# Check for proper loadings
print("Number of Nodes: {}".format(all_inter_graphs["starwars-episode-6-interactions-allCharacters.json"].number_of_nodes()))
print("Number of Edges: {}".format(all_inter_graphs["starwars-episode-6-interactions-allCharacters.json"].number_of_edges()))


