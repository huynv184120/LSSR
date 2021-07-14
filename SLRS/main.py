
import os, sys
import random
from networkx.exception import NetworkXNoCycle

from networkx.generators.classic import null_graph
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
G = nx.DiGraph()

pathFiles = os.listdir('2016TopologyZooUCL_inverseCapacity')
capa = []
sp = None
nNodes = 0
nEdges = 0
loadOptimizer = None

def CreateGraph(path1):
    global nNodes,nEdges
    with open(path1)as f:
        line = f.readline()
        line = line.split()
        nNodes = int(line[1])
        f.readline()
        for i in range(nNodes):
            line = f.readline()
            line = line.split() 
            G.add_nodes_from([(i, {'label' : line[0], 'x' : float(line[1]), 'y' : float(line[2])})])
        f.readline()
        line = f.readline()
        line = line.split()
        nEdges = int(line[1])
        f.readline()
        for i in range(nEdges):
            line = f.readline()
            line = line.split()
            u = int(line[1])
            v = int(line[2])
            w = int(line[3])
            G.add_weighted_edges_from([(u, v, w)])
            G.edges[u ,v]['label'] = line[0]
            G.edges[u ,v]['bw'] = float(line[4])
            G.edges[u ,v]['delay'] = float(line[5])
            G.edges[u, v]['index'] = i
            capa.append(float(line[4]))
        f.close()

def createDemandData(path):
    with open(path)as f:
        line = f.readline()
        line = line.split()
        nDemands = int(line[1])
        f.readline()
        for i in range(nDemands):
            line = f.readline()
            line = line.split()   
            labels.append(line[0])
            srcs.append(int(line[1]))
            dests.append(int(line[2]))
            bws.append(float(line[3]))


        

net = ''
index = 0



for i in range(len(pathFiles)):
    p = pathFiles[i].split('.')

    if(len(p) == 3):
        if net != p[0]:
            index = 0
            net = p[0]
            G.clear()
            capa = []
            pathFile =  '.\\2016TopologyZooUCL_inverseCapacity'+ '\\' + p[0] + '.graph'
            CreateGraph(pathFile)
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
            sp = ShortestPaths(sPathNode, sPathEdge, nSPath)
            capacity =  CapacityData(capa)
        
        srcs = []
        dests = []
        labels = []
        bws = []

        createDemandData('.\\2016TopologyZooUCL_inverseCapacity\\'+pathFiles[i])

        demandData = DemandsData(labels, srcs, dests, bws)
        if index == 0:
            loadOptimizer = LoadOptimizer(sp, capacity, nNodes, nEdges, demandData)
        else:
            loadOptimizer.modifierDemands(demandData)
        # loadOptimizer = LoadOptimizer(sp, capacity, nNodes, nEdges, demandData)


        resultState = loadOptimizer.solve(1000)

        print(p[0], ' ', index, ' ',resultState.trials[2].score())

        f =  open('output5.txt','a')
        s = str(p[0]) + ' '+ str(index) + ' '+ str(resultState.trials[2].score()) + '\n'
        f.write(s)
        f.close()
        index += 1



     

    

        
        





        # line = 0
    #     for row in InFNodes:
    #         if line != 0:
    #             row = str.split(row[0])
    #             G.add_nodes_from([(line-1, {1 : 0})])
    #             {'label' : row[0], 'x' : float(row[1]), 'y' : float(row[2])})])
    #         line += 1
    

    
    # with open(path2)as f:
    #     InFNodes = csv.reader(f)
    #     line = 0
    #     for row in InFNodes:
    #         if line != 0:
    #             row = str.split(row[0])
    #             u = int(row[1])
    #             v = int(row[2])
    #             w = int(row[3])
    #             G.add_weighted_edges_from([(u, v, w)])
    #             G.edges[u ,v]['label'] = row[0]
    #             G.edges[u ,v]['bw'] = float(row[4])
    #             G.edges[u ,v]['delay'] = float(row[5])
    #             G.edges[u, v]['index'] = line-1
    #             capa.append(float(row[4]))
                
    #         line += 1




# nEdges = len(list(G.edges))
# nNodes = len(list(G.nodes))

# sPathNode = []
# sPathEdge = []
# nSPath = []
# for u in G.nodes:
#     A = []
#     B = []
#     C = []
#     for v in G.nodes:
#         A.append( list(nx.all_shortest_paths(G, u , v)))
#         B.append([])
#         C.append(0)
#         if len(A[-1][0]) >= 2:
#             C[-1] = len(A[-1])
#             for path in A[-1]:
#                 B[-1].append([])
#                 for i in range(len(path) - 1):
#                     B[-1][-1].append(G[path[i]][path[i+1]]['index'])

#     sPathNode.append(A)
#     sPathEdge.append(B)
#     nSPath.append(C)


# sp = ShortestPaths(sPathNode, sPathEdge, nSPath)
# capacity =  CapacityData(capa)


# def createDemandData(path):

#     with open(path)as f:
#         InFNodes = csv.reader(f)
#         line = 0
#         for row in InFNodes:
#             if line != 0:
#                 row = str.split(row[0])
#                 labels.append(row[0])
#                 srcs.append(int(row[1]))
#                 dests.append(int(row[2]))
#                 bws.append(float(row[3]))
#             line += 1
# createDemandData('.\data\demandData.csv')


# demandData = DemandsData(labels, srcs, dests, bws)


# loadOptimizer = LoadOptimizer(sp, capacity, nNodes, nEdges, demandData)


# print('first value is ', loadOptimizer.maxLoad.score())
# resultState = loadOptimizer.solve(2000)
# print('optimized value is ', resultState.trials[2].score())
