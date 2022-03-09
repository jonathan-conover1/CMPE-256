#%%
# Imports here | some to be used later
from datetime import date
import numpy as np
import os
import json
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import normalize
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

def sim_rank_pd(graph1):

    sim_rank = nx.simrank_similarity(graph1)
    names = list(graph1.nodes)
    sim_rank_pd = pd.DataFrame(columns=names, index=names)
    for key1 in sim_rank.keys():
        for key2 in sim_rank[key1].keys():
            sim_rank_pd.at[key1,key2] = sim_rank[key1][key2]
        
    return sim_rank_pd
    

# %%
# Initial cluster without normalization
graph = all_inter_graphs["starwars-episode-4-interactions-allCharacters"]
k = 7

sim_rank = sim_rank_pd(graph)
print(sim_rank)

clust = KMeans(n_clusters=k).fit(sim_rank)

clusters = {}
for i in range(len(clust.labels_)):
    try:
        clusters[clust.labels_[i]].append(sim_rank.columns.values[i])
    except:
        clusters[clust.labels_[i]] = [sim_rank.columns.values[i]]
    
for i in clusters:
    print('cluster',i)
    print(clusters[i])

# %%
## Cluster with MinMax preprocessing

min_max = MinMaxScaler()


sim_rank[:] = min_max.fit_transform(sim_rank[:])
sim_rank


clust = KMeans(n_clusters=k).fit(sim_rank)

clusters = {}
for i in range(len(clust.labels_)):
    try:
        clusters[clust.labels_[i]].append(sim_rank.columns.values[i])
    except:
        clusters[clust.labels_[i]] = [sim_rank.columns.values[i]]
    
for i in clusters:
    print('cluster',i)
    print(clusters[i])


print(graph.nodes)


# %%
