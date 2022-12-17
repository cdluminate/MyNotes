#!/usr/bin/python3
import networkx as nx
import matplotlib.pyplot as plt

# init graph and configure
G = nx.DiGraph();
G.add_nodes_from (range(10)); # 6 nodes
G.add_edge (0,5)

G.add_edge (1,6)
G.add_edge (1,7)

G.add_edge (2,5)
G.add_edge (2,6)
G.add_edge (2,8)

G.add_edge (3,7)
G.add_edge (3,8)

G.add_edge (4,7)
G.add_edge (4,9)

G.add_edge (5,0)
G.add_edge (5,2)

G.add_edge (6,1)
G.add_edge (6,2)

G.add_edge (7,1)
G.add_edge (7,3)
G.add_edge (7,4)

G.add_edge (8,2)
G.add_edge (8,3)

G.add_edge (9,4)

nx.draw_networkx (G);
plt.show();
print ("G: caculating dijkstra path from node 0 -> 9")
thepath = nx.dijkstra_path(G,0,9)

#sumweight = 0
for i in range(0, len(thepath)-1):
	print ("i(%d) -> i+1(%d)" % (thepath[i], thepath[i+1]), G.edge[thepath[i]][thepath[i+1]])
	#sumweight = sumweight + G.edge[thepath[i]][thepath[i+1]]['weight']
print ("G: the dijkstra path is")
print (nx.dijkstra_path(G,0,9))
for item in nx.all_simple_paths(G,0,9):
	print (item)
#print ("G: the dijkstra path costs %d" % (sumweight))
#print (nx.dijkstra_path_length(G,0,9))
