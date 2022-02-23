#%%
# Imports here | some to be used later
from cmath import exp
from datetime import date
import numpy as np
import os
import json
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
from scipy.spatial.distance import cosine
#%% 
all_star_wars = {}
movies = Path('data/')
for movie in movies.iterdir():
    if 'mentions' in movie.name and 'starwars-full' not in movie.name:
        with open(movie.resolve()) as f:
            key = movie.name.replace('.json','')
            all_star_wars[key] = json.load(f)
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
            holistic_interaction.add_edge(all_star_wars[key]['nodes'][edge['source']]['name'], 
                                        all_star_wars[key]['nodes'][edge['target']]['name'],
                                        weight=edge['value'] )

    all_inter_graphs[key] = holistic_interaction


# %%
# Check for proper loadings
print("Number of Nodes: {}".format(all_inter_graphs["starwars-episode-6-mentions"].number_of_nodes()))
print("Number of Edges: {}".format(all_inter_graphs["starwars-episode-6-mentions"].number_of_edges()))
print("Luke: {}".format(all_inter_graphs["starwars-episode-6-mentions"].nodes['LUKE']['Amount of Scences']))



# %%

# Visualize the graph connections
options = {
    'node_color': 'green',
    'node_size': 100,
    'width': 1,
    'with_labels': True
}

fig = plt.figure(1, figsize=(20, 10), dpi=90)
nx.draw_kamada_kawai(all_inter_graphs["starwars-episode-6-mentions"], **options)

# %%

def sim_rank_pd(graph1):

    sim_rank = nx.simrank_similarity(graph1)
    names = list(graph1.nodes)
    sim_rank_pd = pd.DataFrame(columns=names, index=names)
    for key1 in sim_rank.keys():
        for key2 in sim_rank[key1].keys():
            sim_rank_pd.at[key1,key2] = sim_rank[key1][key2]
        
    return sim_rank_pd
    
def calc_sim_rank(graph1, graph2):
    graph1_pd = sim_rank_pd(graph1)
    graph2_pd = sim_rank_pd(graph2)

    graph1_pd, graph2_pd = combine(graph1_pd,graph2_pd)

    for col in graph1_pd.columns.values:
        try:
            print(1-cosine(graph1_pd[col],graph2_pd[col]))
            print('ok')
        except:
            pass

def combine(pd1,pd2):
    ind1 = pd1.index.values
    ind2 = pd2.index.values

    combined_ind = np.append(ind1,ind2)
    combined_ind = np.unique(combined_ind)
    new_pd1 = pd.DataFrame(index=combined_ind)
    new_pd2 = pd.DataFrame(index=combined_ind)

    new_pd1 = new_pd1.join(pd1)
    new_pd2 = new_pd2.join(pd2)

    new_pd1.fillna(0,inplace=True)
    new_pd2.fillna(0,inplace=True)

    return new_pd1, new_pd2
    

# %%
calc_sim_rank(all_inter_graphs["starwars-episode-1-mentions"],all_inter_graphs["starwars-episode-5-mentions"])



# %%
