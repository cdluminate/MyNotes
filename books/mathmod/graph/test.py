#!/usr/bin/python3
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph();
G.add_nodes_from ([1,2,3,4,5,6]);
G.add_cycle ([1,2,3,4]);
G.add_edge (1,3,weight=8)
G.add_edges_from ([(3,5),(3,6),(6,7)]);
nx.draw_networkx (G);
plt.savefig("test.eps");
plt.show();
print ("the shortest path from G -> 1")
print (nx.shortest_path(G,1))
print ("the minimum spanning tree")
nx.draw_networkx (nx.minimum_spanning_tree (G))
plt.show();
print ("cycle basis")
print (nx.cycle_basis(G))
#print ("simple cycles")
#print (nx.simple_cycles(G))

