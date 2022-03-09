#%%
# Imports here | some to be used later
from cmath import sqrt
import numpy as np
import os
import json
import networkx as nx
import matplotlib.pyplot as plt

#%%
# load the json file and verify contents

file_list = []
file_list.append("./CMPE-256/data/starwars-episode-1-interactions.json")
file_list.append("./CMPE-256/data/starwars-episode-2-interactions.json")
file_list.append("./CMPE-256/data/starwars-episode-3-interactions.json")
file_list.append("./CMPE-256/data/starwars-episode-4-interactions.json")
file_list.append("./CMPE-256/data/starwars-episode-5-interactions.json")
file_list.append("./CMPE-256/data/starwars-episode-6-interactions.json")
file_list.append("./CMPE-256/data/starwars-episode-7-interactions.json")
file_list.append("./CMPE-256/data/starwars-full-interactions.json")

# %%
# Run for all movies

most_pop_3 = []
least_pop_3 = []

for file_dir in file_list:

    with open(file_dir) as f:
        data = json.load(f)

    #print(data['nodes'][0])
    #print(data['links'][0])

    ## %%
    # Generate an undirected graph
    undirected_G = nx.Graph()

    #build graph nodes
    for node in data['nodes']:
        undirected_G.add_node(node['name'])
        
    #build graph edges
    for edge in data['links']:
        undirected_G.add_edge(data['nodes'][edge['source']]['name'], data['nodes'][edge['target']]['name'])


    ## %%
    sorted_chars = sorted(nx.degree_centrality(undirected_G).items(), key=lambda x : x[1], reverse=True)
    sorted_chars_rounded = list(map(lambda x: [x[0], round(x[1],2)], sorted_chars))
    #print(sorted_chars_rounded[0:3] )
    most_pop_3.append( sorted_chars_rounded[0:3] )
    least_pop_3.append( sorted_chars_rounded[len(sorted_chars_rounded)-3:len(sorted_chars_rounded)] )

    ## %%

# %%
most_pop_3_combined = most_pop_3[7]
most_pop_3.pop(7)
least_pop_3_combined = least_pop_3[7]
least_pop_3.pop(7)

print(most_pop_3)
print(least_pop_3)
print("----")
print(most_pop_3_combined)
print(least_pop_3_combined)

# %%
# Calculate most popular by averaging over each movie
# Then compare to total data

most_pop_dict = {}
least_pop_dict = {}

for movie in most_pop_3:
    for char in movie:
        most_pop_dict[char[0]] = 0
for movie in most_pop_3:
    for char in movie:
        most_pop_dict[char[0]] = most_pop_dict[char[0]] + 1

for movie in least_pop_3:
    for char in movie:
        least_pop_dict[char[0]] = 0
for movie in least_pop_3:
    for char in movie:
        least_pop_dict[char[0]] = least_pop_dict[char[0]] + 1


# Find most popular out of all the movies in the combined dataset
print( most_pop_dict)
print( least_pop_dict)

# %%
# Get most popular
most_pop_val = 0
for key in most_pop_dict:
    if( most_pop_dict[key] > most_pop_val):
        most_pop_val = most_pop_dict[key]

most_pop_over_all_episodes = []
for key in most_pop_dict:
    if( most_pop_dict[key] == most_pop_val):
        most_pop_over_all_episodes.append( key)


print("Most popular over each episode:", most_pop_over_all_episodes )
print("Most popular from combined dataset:", most_pop_3_combined)
# %%
