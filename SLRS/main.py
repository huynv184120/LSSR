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
    G.sp = sp
    G.capacity = capacity
    return G

G = createGraph('data\\abilene_tm_node.csv','data\\abilene_tm_edge.csv')

loadOptimizer = LoadOptimizer(sp, capacity, nNodes, nEdges)

TM = np.random.randint(0,10000,(12,12))
loadOptimizer.modifierTrafficMatrix(TM)

loadOptimizer.solve(1000)


# for path in loadOptimizer.extractRoutingPath():
#     print(path)
# print (loadOptimizer.maxLoad.score())



def computeMaximumLinkUtilization(G, srPaths ,TM):
    MaximumLinkUtilization = 0
    values = [0]*G.number_of_edges()
    for i in range(G.number_of_nodes()):
        for j in range(G.number_of_nodes()):
            if i != j:
                for k in range(len(srPaths[i][j])-1):
                    n = srPaths[i][j][k]
                    m = srPaths[i][j][k + 1]

                    paths = G.sp.pathEdges[n][m]
                    nPath = G.sp.nPaths[n][m]
                    if m != n: 
                        increment = TM[i][j] / nPath
                        for path in paths:
                            for edge in path:
                                values[edge] += increment/G.capacity.capacity[edge]
                                if values[edge] > MaximumLinkUtilization:
                                    MaximumLinkUtilization = values[edge]
    return MaximumLinkUtilization


# print(computeMaximumLinkUtilization(G, loadOptimizer.extractRoutingPath(), TM))
def routingSulutionToRoutingMatrix(routingSolution, G):
    nLinks = G.number_of_edges()
    nNodes = G.number_of_nodes()
    routingMatrix = np.zeros((nLinks,nNodes**2))
    for i in range(nNodes):
        for j in range(nNodes):
            if i != j:
                for k in range(len(routingSolution[i][j])-1):
                    n = routingSolution[i][j][k]
                    m = routingSolution[i][j][k + 1]
                    for path in G.sp.pathEdges[m][n]:
                        for link in path:
                            routingMatrix[link][i*nNodes+j] = 1
    return routingMatrix

def computeFlowTrafficLinks(G, routingSolution, trafficMatrix):
    nLinks = G.number_of_edges()
    nNodes = G.number_of_nodes()
    linksLoad = np.zeros((nLinks, 1))
    for i in range(nNodes):
        for j in range(nNodes):
            if i != j:
                for k in range(len(routingSolution[i][j])-1):
                    n = routingSolution[i][j][k]
                    m = routingSolution[i][j][k + 1]
                    paths = G.sp.pathEdges[n][m]
                    nPath = G.sp.nPaths[n][m]
                    if m != n: 
                        increment = trafficMatrix[i][j] / nPath
                        for path in paths:
                            for edge in path:
                                linksLoad[edge] += increment
    return linksLoad

print(computeFlowTrafficLinks(G, loadOptimizer.extractRoutingPath(), TM))

