#%%
# Imports here | some to be used later
from operator import contains
import numpy as np
import os
import json
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

#%% 
all_star_wars = {}
entries = Path('data/')
for entry in entries.iterdir():
    if 'starwars-full' in entry.name:
        pass
    else:
        with open(entry.resolve()) as f:
            all_star_wars[entry.name] = json.load(f)

print(all_star_wars.keys())

# %%
holistic_interaction = nx.Graph()

for key in all_star_wars.keys():
    if 'interactions' in key:
        all_star_wars[key] 
        for node in all_star_wars[key]['nodes']:
            holistic_interaction.add_node(node['name'])
        
        for edge in all_star_wars[key]['links']:
            holistic_interaction.add_edge(all_star_wars[key]['nodes'][edge['source']]['name'], all_star_wars[key]['nodes'][edge['target']]['name'])

# %%
#print("Nodes: {}".format(list(holistic_interaction)))
print("Number of Nodes: {}".format(holistic_interaction.number_of_nodes()))
print("Number of Edges: {}".format(holistic_interaction.number_of_edges()))

# %%
