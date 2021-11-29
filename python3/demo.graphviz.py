'''
http://pygraphviz.github.io/documentation/pygraphviz-1.4rc1/index.html
http://pygraphviz.github.io/documentation/latest/pygraphviz.pdf
http://www.graphviz.org/doc/info/attrs.html

sudo apt install python3-pygraphviz
see also: networkx package
'''

import pygraphviz as gv

# [ Graph initialization ]
G = gv.AGraph() # empty graph
G = gv.AGraph(strict=False, directed=True) # specify dot format
#G = gv.AGraph('file.dot')
G = gv.AGraph('graph {1 -- 2}') # init graph using a string
G = gv.AGraph({'1': {'2': None}})
#G = gv.AGraph(A.handle) # SWIG pointer
#G = gv.AGraph(ranksep='0.1') # setting attributes on creation
del G

# [ Nodes and edges ]
G = gv.AGraph()
G.add_node('a')
G.add_edge('b', 'c')
G.add_nodes_from(['f', 'g', 'h'])

# [ Attributes ]
G.graph_attr['label'] = 'name of graph'
G.node_attr['shape'] = 'circle'
G.edge_attr['color'] = 'red'
G.add_node(1, color='red')
G.add_edge('b', 'c', color='blue')
G.get_node(1).attr['shape'] = 'box'
G.get_edge('b', 'c').attr['color'] = 'green'

# [ Layout and Drawing ]
print(G.string())
G.layout() # add positions to the nodes with a Graphviz layout algo
#G.layout(prog='dot')
#G.draw(f'{__file__}.png') # render the graph to image
#G.draw(f'{__file__}.svg')
#G.draw(f'{__file__}.pdf')

# [ Grpah with image ]
del G
impath = '../../dotfile/nichijou.hakase.jpeg'
G = gv.AGraph(landscape='false', label='Label of graph', labelloc='t')
G.add_node(1, label='1', shape='circle')
G.add_node(2, label='2', shape='box', image=impath, imagescale='both',
        fixedsize='true', height=0.5, width=0.5)
G.add_node(3, label='node 3', xlabel='node 3')
G.layout()
G.draw('x.pdf')
