#!/usr/bin/python3
import networkx as nx
import matplotlib.pyplot as plt

# init graph and configure
G = nx.DiGraph();
G.add_nodes_from (range(5)); # 6 nodes
G.add_edge (0,1,weight=11+5)
G.add_edge (0,2,weight=11+5+6)
G.add_edge (0,3,weight=11+5+6+8)
G.add_edge (0,4,weight=11+5+6+8+11)
G.add_edge (0,5,weight=11+5+6+8+11+18)
G.add_edge (1,2,weight=11+5)
G.add_edge (1,3,weight=11+5+6)
G.add_edge (1,4,weight=11+5+6+8)
G.add_edge (1,5,weight=11+5+6+8+11)
G.add_edge (2,3,weight=12+5)
G.add_edge (2,4,weight=12+5+6)
G.add_edge (2,5,weight=12+5+6+8)
G.add_edge (3,4,weight=12+5)
G.add_edge (3,5,weight=12+5+6)
G.add_edge (4,5,weight=13+5)

#nx.draw_networkx (G);
#plt.show();
print ("G: caculating dijkstra path from node 0 -> 5")
thepath = nx.dijkstra_path(G,0,5)

#sumweight = 0
#for i in range(0, len(thepath)-1):
#	print ("i(%d) -> i+1(%d)" % (thepath[i], thepath[i+1]), G.edge[thepath[i]][thepath[i+1]])
#	sumweight = sumweight + G.edge[thepath[i]][thepath[i+1]]['weight']
#print ("G: the dijkstra path costs %d" % (sumweight))
print (nx.dijkstra_path_length(G,0,5))
