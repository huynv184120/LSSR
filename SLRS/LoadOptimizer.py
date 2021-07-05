import os, sys
from state.EdgeDemandState import EdgeDemandStateTree
lib_path = os.path.abspath(os.path.join('core'))
sys.path.append(lib_path)
from CapacityData import CapacityData

lib_path = os.path.abspath(os.path.join('state'))
sys.path.append(lib_path)
from FlowState import FlowStateRecomputeDAG
from EdgeDemandState import EdgeDemandStateTree
from PathState import PathState

lib_path = os.path.abspath(os.path.join('constraint'))
sys.path.append(lib_path)
from MaxLoad import MaxLoad



class LoadOptimizer:
    def __init__(self, sp, capacity , nNodes, nEdges, decisionDemands):
        self.sp = sp
        self.nDemands = len(decisionDemands)
        self.capacity = capacity
        self.nNodes = nNodes
        self.nEdges = nEdges
        self.decisionDemands = decisionDemands
        self.pathState = PathState(decisionDemands)
        self.flowState = FlowStateRecomputeDAG(nNodes, nEdges, sp, self.pathState, decisionDemands)
        self.maxLoad = MaxLoad(nNodes, nEdges, capacity, self.flowState, sp)
        self.edgeDemandState = EdgeDemandStateTree(self.nDemands, self.nEdges, self.capacity)

    def selectDemand(self):
        edge = self.maxLoad.selectRandomMaxEdge()
        return self.edgeDemandState.selectRandomDemand(edge)



