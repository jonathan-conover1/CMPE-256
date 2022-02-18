#%%
# Just messing around
from typing import Set
import numpy as np
import pandas as pd
import networkx as nx

df = pd.read_csv("./data/games.csv")
df = df.loc[:, ['victory_status', 'moves']]
df = df.loc[df['victory_status'] == 'mate']
print(df.head)

# %%

df = df.iloc[:20,:]

unique_moves = set()
for i, row in df.iterrows():
    moves = row['moves'].split(' ')
    unique_moves.update(moves)


# %%
G = nx.DiGraph()
G.add_nodes_from(unique_moves)


for i, row in df.iterrows():
    moves = row['moves'].split(' ')
    for i in range(len(moves) - 1):
        G.add_edge(moves[i], moves[i+1])


# %%
options = {
    'node_color': 'green',
    'node_size': 300,
    'width': 1,
    'with_labels': True
}

nx.draw_kamada_kawai(G, **options)
# %%
nx.draw(G)

#%%
nx.draw_random(G, **options)
#%%  
nx.draw_circular(G, **options)  
#%%
nx.draw_spectral(G, **options)  
#%%
nx.draw_spring(G, **options)
# %%

import matplotlib.pyplot as plt
fig = plt.figure(1, figsize=(40, 20), dpi=90)
nx.draw_kamada_kawai(G, **options)

# %%
