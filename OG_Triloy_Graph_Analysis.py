"""
StarWars Social Network database is split into multiple files for each Episode by mention and Character interactions.
Using pandas to load the data in 
"""

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
with open('./data/starwars-episode-4-interactions-allCharacters.json') as f:
    data = json.load(f)

print(data['nodes'][0])
print(data['links'][0])

# %%
# Generate an undirected graph
sw_ep4_graph = nx.Graph()

#build graph nodes
for node in data['nodes']:
    sw_ep4_graph.add_node(node['name'])
    
#build graph edges
for edge in data['links']:
    sw_ep4_graph.add_edge(data['nodes'][edge['source']]['name'], data['nodes'][edge['target']]['name'])

# remove the solo disconnected node
sw_ep4_graph.remove_node("GOLD FIVE")

# Print out to verify data
print("Nodes: {}".format(list(sw_ep4_graph)))
print("Number of Nodes: {}".format(sw_ep4_graph.number_of_nodes()))
print("Number of Edges: {}".format(sw_ep4_graph.number_of_edges()))

# %%
# Visualize the graph connections
options = {
    'node_color': 'green',
    'node_size': 100,
    'width': 1,
    'with_labels': True
}

fig = plt.figure(1, figsize=(20, 10), dpi=90)
nx.draw_kamada_kawai(sw_ep4_graph, **options)

#%%
"""
    Simple Graphing function for visualizing Degree and Ranks
"""
def BarGraphData(data: list, title: str, x_label: str, y_lable: str):
    x_val = [x[0] for x in data]
    y_val = [x[1] for x in data]

    # function to add value labels
    def addlabels(x,y):
        for i in range(len(x)):
            plt.text(i,y[i],y[i])

    # Set the size
    plt.figure(figsize = (30, 15))
    plt.bar(x_val, y_val)
        
    # calling the function to add value labels
    addlabels(x_val, y_val)
        
    # giving title to the plot
    plt.title(title)

    # giving X and Y labels
    plt.xlabel(x_label)
    plt.ylabel(y_lable)
        
    # visualizing the plot
    plt.show()

# %%
# Degree 
print(sw_ep4_graph.degree["OBI-WAN"])
degree = sorted(sw_ep4_graph.degree, key=lambda x: x[1], reverse=True)

# Lets see it
BarGraphData(degree, "Degree", "Characters", "Degree Values")

# %%
# Page Ranks
page_ranks = nx.pagerank(sw_ep4_graph) # A dictionary
print(page_ranks["OBI-WAN"])
ranks = sorted(page_ranks.items(), key=lambda x: x[1], reverse=True)

# Lets see it
BarGraphData(ranks, "Page Rank", "Characters", "Rank Values")

# %%
W = nx.adjacency_matrix(sw_ep4_graph)
print(W.todense())

# %%
# Visualize the Adjacency Matrix
plt.matshow(W.todense())
plt.show()

# %%
# Adj Matrix is in char_list X char_list
char_list = list(sw_ep4_graph)
print(char_list[0:4])
print(char_list[6:11])

# %%
# degree matrix
D = np.diag(np.sum(np.array(W.todense()), axis=1))
print('degree matrix:')
print(D)

# %%
plt.matshow(D)
plt.show()

# %%
# laplacian matrix
L = D - W
print('laplacian matrix:')
print(L)

# %%
# Visualize the Laplacian Matrix
plt.matshow(L)
plt.show()

# %%
e, v = np.linalg.eig(L)
# eigenvalues
print('eigenvalues:')
print(e)

# %%
# eigenvectors
print('eigenvectors:')
print(v)

# %%
fig = plt.figure()
ax1 = plt.subplot(121)
plt.plot(e)
ax1.title.set_text('eigenvalues')
i = np.where(e < 10e-6)[0]
ax2 = plt.subplot(122)
plt.plot(v[:, i[0]])
fig.tight_layout()
plt.show()

# %%
tryout = np.array(v)
plt.matshow(tryout)
plt.show()

# %%
e_v = np.array(v)
first_vector = e_v[:, 8]
print(first_vector)

second_vector = e_v[:, 13]
print(second_vector)

gpr1 = np.where(second_vector < 0)
gpr2 = np.where(second_vector > 0)

for arr in gpr2[0]:
    print(char_list[arr])

# %%
size = len(e)

S = np.full((size, size), 0.0)

second_vector
for i in range(size):
    for ii in range(size):
        x = second_vector[i]**2
        y = second_vector[ii]**2
        S[i][ii] =  x - y

# %%
plt.matshow(S*100)
plt.show()
# %%
print(char_list[14])
print(char_list[15])

# %%
thrid_vector = e_v[:, 14]
print(thrid_vector)

gpr1 = np.where(thrid_vector < 0)
gpr2 = np.where(thrid_vector > 0)

for arr in gpr2[0]:
    print(char_list[arr])
# %%

for i in range(21):
    #19, 16, 15
    plt.plot(e_v[:, i], linestyle='--', marker='o')
    #plt.xlim([0, 20])  
    #plt.ylim([0, 20])  
    plt.xticks(range(0, 21, 1))
    #plt.yticks(range(0, 21, 1))  
    plt.title('eigenvector: {}'.format(i))
    plt.axhline(0, color='r')
    plt.show()

# %%

def eigenGap(e):
    gap = []
    for i in range(len(e) - 1):
        gap.append(abs(e[i] - e[i+1]))
    return gap

e_gap = eigenGap(e)

# %%
plt.plot(e_gap, linestyle='--', marker='o')
plt.xlim([0, 20])  
#plt.ylim([0, 20])  
plt.xticks(range(0, 21, 1))
#plt.yticks(range(0, 21, 1))  
plt.title('eigen gap')
plt.axhline(0, color='r')
plt.show()
# %%
