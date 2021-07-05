from abc import ABC, abstractmethod
from state.PathState import Path
from ArrayState import ArrayStateFloat
import math

class FlowStateChecker(ArrayStateFloat):
    def __init__(self, nNodes, nEdges, pathState, demandsData):
        super().__init__(nNodes)
        self.nNodes = nNodes
        self. nEdges = nEdges
        self.pathState = pathState
        self.demandsData = demandsData

    def check(self):
        self.updateState()
        super.check()

    @abstractmethod
    def modify(self, src, dest, bw):
        pass

    def initialize(self):
        demand = self.pathState.nDemands
        while demand > 0:
            demand -= 1
            path = self.pathState.path(demand)
            pos = self.pathState.size(demand) - 1

            while pos > 0:
                pos -= 1
                src = path[pos]
                dest = path[pos+1]
                self.modify(src, dest, self.demandsData.demandTraffics[demand])

    def updateState(self):
        pChanged = self.pathState.nChanged
        changed = self.pathState.changed
        while pChanged > 0:
            pChanged -= 1
            demand = changed[pChanged]
            bandwidth = self.demandsData.demandTraffics[demand]

            currentPath = self.pathState.path(demand)
            currentSize = self.pathState.size(demand)
            oldPath = self.pathState.oldPath(demand)
            oldSize = self.pathState.oldSize(demand)

            minSize = min(oldSize, currentSize)

            firstDiff = 1

            while firstDiff < minSize & currentPath[firstDiff] == oldPath[firstDiff]:
                firstDiff += 1

            endCurrent = currentSize - 2
            endOld     = oldSize - 2

            while (firstDiff < endCurrent) & (firstDiff < endOld) & (currentPath[endCurrent] == oldPath[endOld]):
                endCurrent -= 1
                endOld -=1

            p = firstDiff - 1
            while p <= endCurrent:
                self.modify(currentPath[p], currentPath[p+1], bandwidth)
                p += 1
            
            q = firstDiff - 1
            while q <= endOld:
                self.modify(oldPath[q], oldPath[q+1], -bandwidth)
                q += 1

class FlowStateRecomputeDAG(FlowStateChecker):
    def __init__(self, nNodes, nEdges, sp, pathState, demandsData):
        super().__init__(nNodes, nEdges, pathState, demandsData)
        self.sp = sp
        self.initialize()
        self.commitState()
    
    def modify(self, src, dest, bw):
        assert src != dest
        paths = self.sp.pathEdges[src][dest]
        nPaths = self.sp.nPaths[src][dest]
        increment = bw / nPaths
        for path in paths:
            for edge in path:
                self.updateValue(edge, self.values[edge] + increment)


            