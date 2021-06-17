from os import close
import csv
import networkx as nx
import numpy as np
from MyStructures import *

G = nx.DiGraph()

n = 0 # number node
m = 0 # number edge
def CreateGraph(path1, path2):
    with open(path1)as f:
        InFNodes = csv.reader(f)
        line = 0
        for row in InFNodes:
            if line != 0:
                row = str.split(row[0])
                k = int(row[0].split('_')[0])
                G.add_nodes_from([(k, {'label' : row[0], 'x' : float(row[1]), 'y' : float(row[2])})])
            line =+ 1
        n = line - 1
    
    with open(path2)as f:
        InFNodes = csv.reader(f)
        line = 0
        for row in InFNodes:
            if line != 0:
                row = str.split(row[0])
                u = int(row[1])
                v = int(row[2])
                w = int(row[3])
                G.add_weighted_edges_from([(u, v, w)])
                G.edges[u ,v]['label'] = row[0]
                G.edges[u ,v]['bw'] = float(row[4])
                G.edges[u ,v]['delay'] = float(row[5])
            line =+ 1
        m = line - 1
CreateGraph('.\data\\abilene_tm_node.csv','.\data\\abilene_tm_edge.csv')

# shortest path
stPathDisc = {}
stPath = []
def toKey(u , v):
    return str(u) + ' ' + str(v)

for u in G.nodes:
    A = []
    for v in G.nodes:
        stPathDisc[toKey(u,v)] = list(nx.all_shortest_paths(G, u , v ))
        A.append( list(nx.all_shortest_paths(G, u , v )))
    stPath.append(A)
print(stPath)
print(stPathDisc.items())
# A = CaculateTree([[1,2],[3,2],[2,2],[4,2]])
# A.addNode(5,1)
# A.showInfor()
# A.delete(3)
# A.delete(5)
# A.showInfor()
