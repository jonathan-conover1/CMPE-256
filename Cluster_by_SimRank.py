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
    if 'interactions' in movie.name and 'starwars-full' not in movie.name:
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
    if 'interactions' in key:
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
print("Number of Nodes: {}".format(all_inter_graphs["starwars-episode-6-interactions"].number_of_nodes()))
print("Number of Edges: {}".format(all_inter_graphs["starwars-episode-6-interactions"].number_of_edges()))
print("Luke: {}".format(all_inter_graphs["starwars-episode-6-interactions"].nodes['LUKE']['Amount of Scences']))



# %%

# Visualize the graph connections
options = {
    'node_color': 'green',
    'node_size': 100,
    'width': 1,
    'with_labels': True
}

fig = plt.figure(1, figsize=(20, 10), dpi=90)
nx.draw_kamada_kawai(all_inter_graphs["starwars-episode-1-interactions"], **options)


# %%

def sim_rank_pd(graph1):

    sim_rank = nx.simrank_similarity(graph1)
    names = list(graph1.nodes)
    sim_rank_pd = pd.DataFrame(columns=names, index=names)
    for key1 in sim_rank.keys():
        for key2 in sim_rank[key1].keys():
            sim_rank_pd.at[key1,key2] = sim_rank[key1][key2]
        
    return sim_rank_pd
    

    

# %%
sim_rank = sim_rank_pd(all_inter_graphs["starwars-episode-1-interactions"])
sim_rank

# %%
from sklearn.preprocessing import MinMaxScaler
norm = MinMaxScaler()


sim_rank[:] = norm.fit_transform(sim_rank[:])
sim_rank
# %%
from sklearn.cluster import KMeans

clust = KMeans(n_clusters=9).fit(sim_rank)

clusters = {}
for i in range(len(clust.labels_)):
    try:
        clusters[clust.labels_[i]].append(sim_rank.columns.values[i])
    except:
        clusters[clust.labels_[i]] = [sim_rank.columns.values[i]]
    
# %%
for i in clusters:
    print('cluster',i)
    print(clusters[i])



# %%
