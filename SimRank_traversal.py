#%% 
from datetime import date
from operator import index
import numpy as np
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
    if 'starwars-full' not in movie.name and 'allCharacters' not in movie.name and 'mentions' not in movie.name:
        with open(movie.resolve()) as f:
            key = movie.name.replace('.json','')
            all_star_wars[key] = json.load(f)
    else:
        pass
        
print(all_star_wars.keys())

#%%
inter_graphs = {}
for key in all_star_wars.keys():
    ana_var = 0
    ana_var_edges = []
    if 'interactions' in key:
        holistic_interaction = nx.Graph()
        
        for node in all_star_wars[key]['nodes']:
            if 'ANAKIN' in node['name'] or 'DARTH VADER' in node['name']:
                ana_var +=node['value']
            else:
                holistic_interaction.add_node(node['name'])
                nx.set_node_attributes(holistic_interaction,{node['name']:node['value']}, name="Amount of Scences")

        holistic_interaction.add_node("ANAKIN/VADER")
        nx.set_node_attributes(holistic_interaction,{"ANAKIN/VADER":ana_var}, name="Amount of Scences")
        
        for edge in all_star_wars[key]['links']:
            src_name = all_star_wars[key]['nodes'][edge['source']]['name']
            dest_name = all_star_wars[key]['nodes'][edge['target']]['name']
            
            if 'ANAKIN' in src_name or "DARTH VADER" in src_name:
                src_name = "ANAKIN/VADER"
            elif 'ANAKIN' in dest_name or "DARTH VADER" in dest_name:
                dest_name = "ANAKIN/VADER"

            holistic_interaction.add_edge(src_name,dest_name,weight=edge['value'])
        
                
        

    inter_graphs[key] = holistic_interaction




# %%
# Check for proper loadings
print("Number of Nodes: {}".format(inter_graphs["starwars-episode-6-interactions"].number_of_nodes()))
print("Number of Edges: {}".format(inter_graphs["starwars-episode-6-interactions"].number_of_edges()))
print("ANAKIN/VADER: {}".format(inter_graphs["starwars-episode-3-interactions"].nodes['ANAKIN/VADER']['Amount of Scences']))



# %%

def sim_rank_pd(who,ignore):
    sim_dict = {}
    for i in all_star_wars.keys():
        if i not in ignore:
                
            sim_rank = nx.simrank_similarity(inter_graphs[i], source=who)
            sim_rank_pd = pd.DataFrame(data=sim_rank.values(),index=sim_rank.keys())
            sim_rank_pd.rename({0:'ANAKIN/VADER'},inplace=True,axis=1)
            sim_rank_pd.drop(axis=0,labels="ANAKIN/VADER",inplace=True)
            sim_rank_pd.sort_values(by='ANAKIN/VADER',axis=0, inplace=True,ascending=False)
            sim_dict[i] = sim_rank_pd

    return sim_dict

# %%
sim_rank_by_movie = sim_rank_pd('ANAKIN/VADER','starwars-episode-7-interactions')
print(sim_rank_by_movie["starwars-episode-5-interactions"])


# %%
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

def calc_sim_rank(graph1, graph2):
    
    graph1_pd, graph2_pd = combine(graph1,graph2)

    for col in graph1_pd.columns.values:
        cos = 1-cosine(graph1_pd[col],graph2_pd[col])

    return cos

# %%
movies = list(sim_rank_by_movie.keys())
all_cos = {}
for i in range(len(movies)-1):
    cos = calc_sim_rank(sim_rank_by_movie[movies[i]],sim_rank_by_movie[movies[i+1]])
    cur_key = str('-'.join(movies[i].split('-')[1:3])+" and "+'-'.join(movies[i+1].split('-')[1:3]))
    all_cos[cur_key] = cos
        
        

cos_pd = pd.DataFrame(data = all_cos.values(),index=all_cos.keys())
cos_pd.rename({0:'Cosine Similarity'},inplace=True,axis=1)
cos_pd



# %%
