from typing import overload
from TrialState import TrialState

class ArrayStateFloat(TrialState):
    def __init__(self, nElements):
        super().__init__()
        self.nElements = nElements
        self.values = [0.0]*nElements
        self.oldValues = [0.0]*nElements
        self.deltaMarker = [False]*nElements
        self.deltaElements = [-1]*nElements
        self.nDelta = 0
    
    def updateValue(self, element, newValue):
        if self.deltaMarker[element] == False:
            self.deltaMarker[element] == True
            self.deltaElements[element] = element
            self.nDelta += 1
        self.values(element) = newValue

    def revertState(self):
        while self.nDelta > 0:
            self.nDelta -= 1
            element = self.deltaElements[self.nDelta]
            self.deltaMarker[self.nDelta] = False
            self.values[element] = self.oldValues[element]

    def commitState(self):
        while self.nDelta > 0:
            self.nDelta -= 1
            element = self.deltaElements[self.nDelta]
            self.deltaMarker[self.nDelta] = False
            self.oldValues[element] =  self.values[element]
