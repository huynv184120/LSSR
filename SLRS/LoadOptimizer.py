import os, sys

from networkx.classes.function import neighbors
from state.SavedState import SavedState
from state.EdgeDemandState import EdgeDemandStateTree
lib_path = os.path.abspath(os.path.join('core'))
sys.path.append(lib_path)
from CapacityData import CapacityData
import random
import time


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
        self.nDemands = decisionDemands.nDemands
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

        
        self.neighborhoods = [Reset(self.pathState), Remove(self.pathState), Insert(self.nNodes, self.pathState), Replace(self.nNodes, self.pathState)]
        self.kickNeighborhoods = [Reset(self.pathState), Remove(self.pathState)]



    def selectDemand(self):
        edge = self.maxLoad.selectRandomMaxEdge()
        return self.edgeDemandState.selectRandomDemand(edge)



    def visitNeighborhood(self, neighborhood, setter):
        nBestMoves = 0
        bestNeighborhoodLoad = 999999999.0
        improvementFound = False
        neighborhood.setNeighborhood(setter)
        while neighborhood.hasNext():
            neighborhood.next()
            neighborhood.apply()
            
            
            if (self.pathState.nChanged > 0 & self.pathState.check()):
                score = self.maxLoad.score()
                
                if (score == bestNeighborhoodLoad):
                    nBestMoves += 1
                    if (random.randint(0, nBestMoves) == 0):
                        neighborhood.saveBest()
                else:
                    if (score < bestNeighborhoodLoad):
                        nBestMoves = 1
                        improvementFound = True
                        neighborhood.saveBest()
                        bestNeighborhoodLoad = self.maxLoad.score()
                self.pathState.revert()
        


        return improvementFound

    def kick(self, demand):
        choice = random.randint(0, self.kickNeighborhoods)
        neighborhood = self.kickNeighborhoods[choice]
        if self.visitNeighborhood(neighborhood, demand):
            neighborhood.applyBest()
            self.pathState.update()
            self.pathState.commit()
    
    def startMoving(self, timeLimit):
        startTime = time.time() * 1000000000
        stopTime  = startTime + timeLimit * 1000000
        bestLoad = self.maxLoad.score()
        nIterations = 0
        bestIteration = 0
        while(time.time() * 1000000000 < stopTime):
            nIterations += 1
            if (self.maxLoad.score() > bestLoad) & (nIterations > (bestIteration + 1000)):
                self.bestPaths.restorePath()
                self.pathState.update()
                self.pathState.commit()
                bestIteration = nIterations - 1

            demand = self.selectDemand()

            if (self.maxLoad.score == bestLoad) & (nIterations > (bestIteration + 3)):
                bestIteration = nIterations
                self.kick(demand)
            
            improvementFound = False
            pNeighborhood = 0
            while (improvementFound == False) & (pNeighborhood < len(self.neighborhoods)):
                neighborhood = self.neighborhoods[pNeighborhood]
                improvementFound = self.visitNeighborhood(neighborhood, demand)
                if improvementFound:
                    neighborhood.applyBest()
                    self.pathState.update()
                    self.pathState.commit()
                    
                    if self.maxLoad.score() < bestLoad:
                        self.bestPaths.savePath()
                        bestLoad = self.maxLoad.score()
                        bestIteration = nIterations

                pNeighborhood += 1
    
    def solve(self,timeLimit):
        self.startMoving(timeLimit)
        print(self.bestPaths.paths)
        self.bestPaths.restorePath()
        self.pathState.update()
        self.pathState.commit()
        print(self.bestPaths.paths)
        return self.pathState




