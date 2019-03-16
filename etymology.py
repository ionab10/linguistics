import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import community
import seaborn as sns
import random 
import numpy as np


df = pd.read_csv("./etymwn-20130208/etymwn.tsv", sep = "\t", header=None, nrows=100000)

iso_lang_codes = pd.read_csv("iso-639-3_Name_Index_20190125.tab", sep = "\t", usecols=['Id', 'Print_Name'])
iso_lang_codes = dict(iso_lang_codes.to_numpy())

G = nx.Graph()

for i,row in df.iterrows():
	if row[1] == "rel:etymology":
		u = row[0].split(":")[0]
		v = row[2].split(":")[0]

		if G.has_edge(u,v):
			G[u][v]['weight']= G[u][v]['weight'] +1
		else:
			G.add_edge(u, v, weight=1)


#G=nx.k_core(G,k=3)
print(nx.info(G))

#community detection
partition = community.best_partition(G)
#positioning
'''init_pos = { i : (random.random(), random.random()) for i in G.nodes()}
forceatlas2 = ForceAtlas2(
						  # Behavior alternatives
						  outboundAttractionDistribution=False,  # Dissuade hubs
						  linLogMode=False,  # NOT IMPLEMENTED
						  adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
						  edgeWeightInfluence=2.0,

						  # Performance
						  jitterTolerance=1.0,  # Tolerance
						  barnesHutOptimize=True,
						  barnesHutTheta=1.2,
						  multiThreaded=False,  # NOT IMPLEMENTED

						  # Tuning
						  scalingRatio=2.0,
						  strongGravityMode=False,
						  gravity=1.0,

						  # Log
						  verbose=True)
						  pos = forceatlas2.forceatlas2_networkx_layout(G, init_pos, iterations=500)'''

pos = nx.spring_layout(G)


size = len(set(partition.values()))
cmap = sns.color_palette("hls", n_colors=size)

#drawing

for i,com in enumerate(set(partition.values())) :
	list_nodes = [nodes for nodes in partition.keys()
	if partition[nodes] == com]
	nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 30, node_color = cmap[i])

labels = {}
for node in G.nodes():
	try:
		labels[node] = iso_lang_codes[node]
	except:
		labels[node] = node
nx.draw_networkx_labels(G, pos, labels = labels)
nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.xticks([])
plt.yticks([])
plt.title("Etymology Graph")

plt.show()