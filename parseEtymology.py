import sys
import re
from bs4 import BeautifulSoup
from ast import literal_eval
import networkx as nx
import matplotlib.pyplot as plt
import community
import seaborn as sns
import random 
import numpy as np
#import cython
#from fa2 import ForceAtlas2


def parse_ety(ety):
	soup = BeautifulSoup(ety, 'lxml').find('ety')

	for x in soup.find_all(True):
		x.extract()

	langs = re.findall('[A-Z][A-Za-z]*\.',soup.text)

	return langs

ety = [
"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<ety>[OE. <ets>hous</ets>, <ets>hus</ets>, AS. <ets>hÔøΩs</ets>; akin to OS. &amp; OFries. <ets>hÔøΩs</ets>, D. <ets>huis</ets>, OHG. <ets>hÔøΩs</ets>, G. <ets>haus</ets>, Icel. <ets>hÔøΩs</ets>, Sw. <ets>hus</ets>, Dan. <ets>huus</ets>, Goth. gud<ets>hÔøΩs</ets>, house of God, temple; and prob. to E. <ets>hide</ets> to conceal. See <er>Hide</er>, and cf. <er>Hoard</er>, <er>Husband</er>, <er>Hussy</er>, <er>Husting</er>.]</ety>\n",
"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<ety>[AS. <ets>hÔøΩsian</ets>.]</ety>\n",
"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<ety>[AS. <ets>cat</ets>; akin to D. &amp; Dan. <ets>kat</ets>, Sw. <ets>katt</ets>, Icel. <ets>k√∂ttr</ets>, G. <ets>katze</ets>, <ets>kater</ets>, Ir. <ets>cat</ets>, W. <ets>cath</ets>, Armor. <ets>kaz</ets>, LL. <ets>catus</ets>, Bisc. <ets>catua</ets>, NGr. <grk>ga`ta</grk>, <grk>ga`tos</grk>, Russ. &amp; Pol. <ets>kot</ets>, Turk. <ets>kedi</ets>, Ar. <ets>qitt</ets>; of unknown origin. Cf. <er>Kitten</er>.]</ety>\n",
"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<ety>[AS. <ets>docga</ets>; akin to D. <ets>dog</ets> mastiff, Dan. <ets>dogge</ets>, Sw. <ets>dogg</ets>.]</ety>\n",
"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<ety>[OE. <ets>book</ets>, <ets>bok</ets>, AS. <ets>b≈çc</ets>; akin to Goth. <ets>b≈çka</ets> a letter, in pl. book, writing, Icel. <ets>b≈çk</ets>, Sw. <ets>bok</ets>, Dan. <ets>bog</ets>, OS. <ets>b≈çk</ets>, D. <ets>boek</ets>, OHG. <ets>puoh</ets>, G. <ets>buch</ets>; and fr. AS. <ets>b≈çc</ets>, <ets>bƒìce</ets>, beech; because the ancient Saxons and Germans in general wrote runes on pieces of beechen board. Cf. <er>Beech</er>.]</ety>\n",
"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<ety>[As. <ets>box</ets>, L. <ets>buxus</ets>, fr. Gr. ÔøΩ. See <er>Box</er> a case.]</ety>\n",
"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<ety>[As. <ets>box</ets> a small case or vessel with a cover; akin to OHG. <ets>buhsa</ets> box, G. <ets>b√ºchse</ets>; fr. L. <ets>buxus</ets> boxwood, anything made of boxwood. See <er>Pyx</er>, and cf. <er>Box</er> a tree, <er>Bushel</er>.]</ety>\n",
"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<ety>[Cf.Dan. <ets>baske</ets> to slap, <ets>bask</ets> slap, blow. Cf. <er>Pash</er>.]</ety>\n",
"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<ety>[Cf.Sp. <ets>boxar</ets>, now spelt <ets>bojar</ets>.]</ety>\n",
"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<ety>[OE. <ets>bagge</ets>; cf. Icel. <ets>baggi</ets>, and also OF. <ets>bague</ets>, bundle, LL. <ets>baga</ets>.]</ety>\n",
"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<ety>[OE. <ets>chaiere</ets>, <ets>chaere</ets>, OF. <ets>chaiere</ets>, <ets>chaere</ets>, F. <ets>chaire</ets> pulpit, fr. L. <ets>cathedra</ets> chair, armchair, a teacher's or professor's chair, Gr. ÔøΩ down + ÔøΩ seat, ÔøΩ to sit, akin to E. <ets>sit</ets>. See <er>Sit</er>, and cf. <er>Cathedral</er>, <er>chaise</er>.]</ety>\n",
"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<ety>[F. <ets>cr√™me</ets>, perh. fr. LL. <ets>crema</ets> cream of milk; cf. L. <ets>cremor</ets> thick juice or broth, perh. akin to <ets>cremare</ets> to burn.]</ety>\n",
]

G = nx.Graph()

for e in ety:
	etym_list=parse_ety(e)
	for i in range(len(etym_list)-1):
		u = etym_list[i]
		v = etym_list[i+1]

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

nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.xticks([])
plt.yticks([])
plt.title("Etymology Graph")

plt.show()