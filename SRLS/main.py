from os import close
import csv
import networkx as nx
import numpy as np
import math
import random as rd

from MyStructures import *

G = nx.DiGraph()
capas = []
nNodes = 0 # number node
nEdges = 0 # number edge
dictEdges = {}

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
            nNodes = line -1

    
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
                G.edges[u, v]['index'] = nEdges
                dictEdges[nEdges] = [u,v]
                capas.append(float(row[4]))
                
            line += 1
            nEdges = line - 1

CreateGraph('.\data\\abilene_tm_node.csv','.\data\\abilene_tm_edge.csv')



mainTree = None
subTree = []
loads = np.zeros(nEdges)
util = np.zeros(nEdges)
capas = np.array(capas)


stPath = []
for u in G.nodes:
    A = []
    for v in G.nodes:
        A.append( list(nx.all_shortest_paths(G, u , v )))
    stPath.append(A)
sp = ShortestPaths(stPath)

def init():
    mainTree = CaculateTree(range(nEdges))
    for i in range(nEdges):
        subTree.append(CaculateTree())

def metaWeight(w, beta):
    return w**beta

def flowCompute(u , v, bw , demandIndex):
    paths = sp.scPath(u,v)
    numSubPaths = len(paths)
    subBw = bw/numSubPaths
    for path in paths:
        for i in range(len(path)-1):
            k = G.edges[path[i]][path[i+1]]
            loads[k] += subBw
            util[k] = loads[k]/capas[k]
            mainTree.setWeightNode(metaWeight(util[k],64))
            if subTree[k].nodeExist(demand):
                if(bw<0):
                    subTree[k].delete(demand)
                else:
                    w = subTree[k].getValueNode(demand)**(1/2)
                    subTree[k].setWeightNode(metaWeight(subBw+w,2))
            else:
                subTree[k].addNode(demand, bw)


def changeDemandData(demands):
    loads = np.zeros(nEdges)
    util = np.zeros(nEdges)
    mainTree.resetValues()
    for tree in subTree:
        tree.removeAllNodes()
    
    for i in range(len(demands)):
        flowCompute(demands[i].src, demands[i].dest, demands[i].bw, i)

def selectDemand():
    edge = mainTree.select()
    demand = subTree[edge].select()
    return demand


def optimize():
    pass


 
