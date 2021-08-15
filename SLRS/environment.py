import os, sys
import random
from networkx.exception import NetworkXNoCycle
import numpy as np
import networkx
lib_path = os.path.abspath(os.path.join('core'))
sys.path.append(lib_path)
from CapacityData import CapacityData

from state.EdgeDemandState import EdgeDemandStateTree

lib_path = os.path.abspath(os.path.join('2016TopologyZooUCL_inverseCapacity'))
sys.path.append(lib_path)
from LoadOptimizer import LoadOptimizer
import csv
import networkx as nx
from networkx.algorithms.centrality import percolation
from ShortestPaths import ShortestPaths

capacity = []
sp = None

def createGraph(NodesFile, EdgesFile):
    global  capacity, sp
    capacity = []
    G =  nx.DiGraph()
    with open(NodesFile) as f:
        f.readline()
        lines = f.readlines()
        for i in range(len(lines)):
            G.add_node(i)
    

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
    G.sp = sp
    G.capacity = capacity
    return G

G = createGraph('data\\abilene_tm_node.csv','data\\abilene_tm_edge.csv')

TM = np.ones((12,12))

def init(G ,TM):
    values = [0]*G.number_of_edges()
    edgeDemandState = EdgeDemandStateTree(G.number_of_nodes()**2, G.number_of_edges(), G.capacity)
    for i in range(G.number_of_nodes()):
        for j in range(G.number_of_nodes()):
            if i != j:
                paths = G.sp.pathEdges[i][j]
                nPath = G.sp.nPaths[i][j]
                increment = TM[i][j] / nPath
                for path in paths:
                    for edge in path:
                        values[edge] += increment/G.capacity.capacity[edge]
                        edgeDemandState.updateEdgeDemand(edge, i*G.number_of_nodes() + j, increment)
    
    return values  # values is utilization 

def selectionDemand(G, edgeDemandState, U ,edge):
    idDemand = edgeDemandState.selectRandomDemand(edge)
    if edgeDemandState.flowOnEdgeDemand(edge, idDemand) < 0.000001:
        u = -1
        v = -1
        return u, v
    u = int(idDemand / G.number_of_nodes())
    v = idDemand % G.number_of_nodes()
    return u,v    

def transitionFunction(G, TM, edgeDemandState, U, u, v, a, edgeMax):
    paths = G.sp.pathEdges[u][v]
    nPath = G.sp.nPaths[u][v]
    oldMaxUtil = U[edgeMax]

    increment = TM[u][v] / nPath
    for path in paths:
        for edge in path:
            U[edge] -= increment/G.capacity.capacity[edge]
            edgeDemandState.updateEdgeDemand(edge, u*G.number_of_nodes() + v, -increment)
    
    paths = G.sp.pathEdges[u][a]
    nPath = G.sp.nPaths[u][a]
    newMaxUtil = 0
    newEdgeMax = 0
    increment = TM[u][v] / nPath
    for path in paths:
        for edge in path:
            U[edge] += increment/G.capacity.capacity[edge]
            if newMaxUtil < U[edge]:
                newMaxUtil = U[edge]
                newEdgeMax = edge

    paths = G.sp.pathEdges[a][v]
    nPath = G.sp.nPaths[a][v]
    increment = TM[u][v] / nPath
    for path in paths:
        for edge in path:
            U[edge] += increment/G.capacity.capacity[edge]
            if newMaxUtil < U[edge]:
                newMaxUtil = U[edge]
                newEdgeMax = edge
    

    changeMaxUtil = oldMaxUtil - U[edgeMax]
    

    if U[edgeMax] < U[newEdgeMax]:
        edgeMax = newEdgeMax

    u, v = selectionDemand(G, edgeDemandState, U, edgeMax)

    return U, (u,v), changeMaxUtil  #U is Utilization (u, v) is demand 




    
