import os, sys
import random
from networkx.exception import NetworkXNoCycle
import numpy as np
import networkx
lib_path = os.path.abspath(os.path.join('core'))
sys.path.append(lib_path)
from CapacityData import CapacityData

lib_path = os.path.abspath(os.path.join('io'))
sys.path.append(lib_path)
from DemandsData import DemandsData

lib_path = os.path.abspath(os.path.join('2016TopologyZooUCL_inverseCapacity'))
sys.path.append(lib_path)
from LoadOptimizer import LoadOptimizer
import csv
import networkx as nx
from networkx.algorithms.centrality import percolation
from ShortestPaths import ShortestPaths

nNodes = 0
nEdges = 0
capacity = []
sp = None

def createGraph(NodesFile, EdgesFile):
    global nNodes, nEdges, capacity, sp
    capacity = []
    G =  nx.DiGraph()
    with open(NodesFile) as f:
        f.readline()
        lines = f.readlines()
        for i in range(len(lines)):
            G.add_node(i)
    
    nNodes = G.number_of_nodes()

    with open(EdgesFile) as f:
        f.readline()
        lines = f.readlines()
        index = 0
        for line in lines:
            line = line.split()
            src = int(line[1])
            dest = int(line[2])
            w = float (line[3])
            capacity.append(float(line[4]))
            G.add_weighted_edges_from([(src, dest, w)])
            G.edges[src,dest]['index'] = index
            index += 1
    
    nEdges = G.number_of_edges()
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
                    for j in range(len(path) - 1):
                        B[-1][-1].append(G[path[j]][path[j+1]]['index'])
        sPathNode.append(A)
        sPathEdge.append(B)
        nSPath.append(C)
    capacity =  CapacityData(capacity)
    sp = ShortestPaths(sPathNode, sPathEdge, nSPath)
    return G

G = createGraph('data\\abilene_tm_node.csv','data\\abilene_tm_edge.csv')

loadOptimizer = LoadOptimizer(sp, capacity, nNodes, nEdges)

TM = np.array(((1,20000000,3),(4,7,3000003),(1,21,1)))
loadOptimizer.modifierTrafficMatrix(TM)

loadOptimizer.solve(1000)

print (loadOptimizer.maxLoad.score())
