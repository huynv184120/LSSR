
from os import close
import os, sys

from networkx.generators.classic import null_graph
lib_path = os.path.abspath(os.path.join('core'))
sys.path.append(lib_path)
from CapacityData import CapacityData

lib_path = os.path.abspath(os.path.join('io'))
sys.path.append(lib_path)
from DemandsData import DemandsData

from LoadOptimizer import LoadOptimizer

import csv
import networkx as nx
from networkx.algorithms.centrality import percolation
from ShortestPaths import ShortestPaths
G = nx.DiGraph()

capa = []

def CreateGraph(path1, path2):
    with open(path1)as f:
        InFNodes = csv.reader(f)
        line = 0
        for row in InFNodes:
            if line != 0:
                row = str.split(row[0])
                k = int(row[0].split('_')[0])
                G.add_nodes_from([(k, {'label' : row[0], 'x' : float(row[1]), 'y' : float(row[2])})])
            line += 1

    
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
                G.edges[u, v]['index'] = line-1
                capa.append(float(row[4]))
                
            line += 1

CreateGraph('.\data\\abilene_tm_node.csv','.\data\\abilene_tm_edge.csv')


nEdges = len(list(G.edges))
nNodes = len(list(G.nodes))

sPathNode = []
sPathEdge = []
nSPath = []
for u in G.nodes:
    A = []
    B = []
    C = []
    for v in G.nodes:
        A.append( list(nx.all_shortest_paths(G, u , v)))
        B.append([])
        C.append(0)
        if len(A[-1][0]) >= 2:
            C[-1] = len(A[-1])
            for path in A[-1]:
                B[-1].append([])
                for i in range(len(path) - 1):
                    B[-1][-1].append(G[path[i]][path[i+1]]['index'])

    sPathNode.append(A)
    sPathEdge.append(B)
    nSPath.append(C)

sp = ShortestPaths(sPathNode, sPathEdge, nSPath)
capacity =  CapacityData(capa)
demandData = DemandsData([1,2,3,4], [1,1,1,1], [6,6,4,7], [20000,2000,200,200])
loadOptimizer = LoadOptimizer(sp, capacity, nNodes, nEdges, demandData)



resultState = loadOptimizer.solve(1000)



print('optimized value is ', resultState.trials[2].score())
