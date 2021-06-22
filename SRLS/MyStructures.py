import numpy as np
from numpy import index_exp, random as rd
from numpy.lib.function_base import insert

class ArrayHeapInt:
    def __init__(self, nValues) :
        self.nValues = nValues
        self.indexLast = 0
        self.values = np.zeros(nValues+1, dtype = int)
        self.indexOf = np.zeros(nValues, dtype = int)
        self.keys = np.zeros(nValues, dtype = int)


    def inHeap(self, value) :
        return self.indexOf[value] != 0
    

    def valueMin(self) :
        if self.indexLast != 0 :
            return self.values[1]
        else :
            print("heap empty")
    

    def keyMin(self) :
        if self.indexLast != 0 :
            return self.keys[self.values[1]]
        else :
            print("empty")
    

    def size(self) :
        return self.indexLast
    

    def isEmpty(self) :
        return self.indexLast == 0
    

    def clear(self) :
        self.indexLast = 0


    def enqueue(self, key, value) :
        assert (self.indexLast <= self.nValues), "heap is full"
        assert (0 <= value & value < self.nValues), "illegal value"
        assert (self.indexOf[value] == 0), "value must not already be in map"
        
        self.indexLast += 1
        self.keys[value] = key
        self.indexOf[value] = self.indexLast
        self.heapifyBottomUp(self.indexLast)


    def dequeue(self):
        value = self.values[1]
        self.indexOf[value] = 0

        if self.indexLast > 1 :
            self.values[1] = self.values[self.indexLast]
            self.indexOf[self.values[1]] = 1
            self.heapifiTopDown(1)
        self.indexLast -= 1

        return value

    def heapifyBottomUp(self, index):
        value = self.values[index]
        key = self.keys[value]

        while index>1 :
            indexParent = index >> 1
            if self.keys[value] <= key :
                break

            self.values[index] = self.values[indexParent]
            self.indexOf[self.values[indexParent]] = index
            index = indexParent

        self.values[index] = value
        self.indexOf[value] = index
        

    def heapifiTopDown(self, index) :
        value = self.values[index]
        key = self.keys[value]
        indexMaxParent = self.indexLast >> 1
        while index <= indexMaxParent  :
            indexMin = self.indexOfMinChild(index)
            valueMin = self.values[indexMin]
            if(self.keys[valueMin] >= key) :
                break
            self.values[index] = self.values[indexMin]
            self.indexOf[self.values[index]] = index
            index = indexMin

        self.values[index] = value
        self.indexOf[value] = index
    

    def indexOfMinChild(self, index):
        indexLeft = index << 1
        assert (indexLeft <= self.indexLast) , "i has no children "
        indexRight = indexLeft + 1

        return (indexRight,indexLeft)[indexRight <= self.indexLast & indexRight <= indexLeft]

    def decreaseKey(self, keyUpdate, value):
        assert (0 <= value & value < self.nValues), "illegal value"
        assert (self.indexOf[value] != 0), "value must be in heap"
        assert keyUpdate < self.keys[value] , "New key must be smaller than old key"

        self.keys[value] = keyUpdate
        self.heapifyBottomUp(self.indexOf[value])




class CaculateTree:

    def __init__(self, arr = None):
        self.dict1 = {}
        self.dict2 = {}
        self.size = 8
        self.n = 0
        self.arr = np.zeros(self.size*2)
        if arr != None:
            while self.size < len(arr):
                self.size *= 2
            for node in arr:
                self.addNode(node[0], node[1])

    def setWeightNode(self, node, w):
        index = self.dict1[node]
        denta = w - self.arr[index]
        while index >= 1:
            self.arr[index] += denta
            index = int(index / 2)
    
    def nodeExist(node):
        return node in self.dict1

    def getValueNode(node):
        return self.arr[self.dict1[node]]

    def addNode(self, node, nodeValue):
        if self.n == self.size :
            self.size *= 2
            arr1 = np.copy(self.arr)
            self.arr = np.zeros(self.size*2)
            self.n = 0
            self.dict1 = {}
            self.dict2 = {}

            for k in self.dict1:
                self.addNode(k, arr1[self.dict1.get(k)])
            
        self.dict1[node] = self.n + self.size
        self.dict2[self.n + self.size] = node
        self.setWeightNode(node, nodeValue)
        self.n +=1

    def delete(self, node):
        
        self.setWeightNode(node, self.arr[self.n+self.size-1])
        
        k =  self.dict1[node]
        node1 = self.dict2[self.n+self.size-1]
        self.setWeightNode(node1 , 0)
        self.dict1[node1] = self.dict1[node]
        self.dict2[k] = node1
        self.dict1.pop(node)
        self.n -= 1

    def select(self):
        n = rd.random()*self.arr[1]
        index = 1
        while index*2 < len(self.n + self.size):
            index = index*2
            if (index + 1 < len(self.n + self.size)) & (n > self.arr[index]):
                n = n - self.arr[index]
                index = index + 1
        return self.dict2[index]

    def showInfor(self):
        print(self.arr)
        
    def resetValues(self):
        for i in range(self.n):
            self.arr[i] = 0

    def removeAllNodes(self):
        self.resetValues()
        self.n = 0
        self.dict1 = {}
        self.dict2 = {}
        
    
class ShortestPaths:
    def __init__(self, paths):
        self.paths = paths
    
    def scPath(self, u, v):
        return self.paths[u][v]


