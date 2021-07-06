import os, sys
from state.SavedState import SavedState
from state.EdgeDemandState import EdgeDemandStateTree
lib_path = os.path.abspath(os.path.join('core'))
sys.path.append(lib_path)
from CapacityData import CapacityData

lib_path = os.path.abspath(os.path.join('state'))
sys.path.append(lib_path)
from FlowState import FlowStateRecomputeDAG , FlowStateRecomputeDAGOnCommit
from EdgeDemandState import EdgeDemandStateTree
from PathState import PathState

lib_path = os.path.abspath(os.path.join('constraint'))
sys.path.append(lib_path)
from MaxLoad import MaxLoad

lib_path = os.path.abspath(os.path.join('neighborhood'))
sys.path.append(lib_path)
from Insert import Insert
from Replace import Replace
from Remove import Remove
from Reset import Reset


class LoadOptimizer:
    def __init__(self, sp, capacity , nNodes, nEdges, decisionDemands):
        self.sp = sp
        self.nDemands = len(decisionDemands)
        self.capacity = capacity
        self.nNodes = nNodes
        self.nEdges = nEdges
        self.decisionDemands = decisionDemands
        self.edgeDemandState = EdgeDemandStateTree(self.nDemands, self.nEdges, self.capacity)
        self.pathState = PathState(decisionDemands)
        self.flowState = FlowStateRecomputeDAG(nNodes, nEdges, sp, self.pathState, decisionDemands)
        self.flowStateOnCommit = FlowStateRecomputeDAGOnCommit(nNodes, nEdges, sp, self.pathState, decisionDemands, self.edgeDemandState)
        self.maxLoad = MaxLoad(nNodes, nEdges, capacity, self.flowState, sp)
        self.bestPaths = SavedState(self.pathState)

        self.pathState.addTrial(self.flowState)
        self.pathState.addTrial(self.flowStateOnCommit)
        self.pathState.addTrial(self.maxLoad)
        self.pathState.addTrial(self.bestPaths)

        
        neighborhoods = [Reset(self.pathState), Remove(self.pathState), Insert(self.nNodes, self.pathState), Replace(self.nNodes, self.pathState)]
        kickNeighborhoods = [Reset(self.pathState), Remove(self.pathState)]



    def selectDemand(self):
        edge = self.maxLoad.selectRandomMaxEdge()
        return self.edgeDemandState.selectRandomDemand(edge)



